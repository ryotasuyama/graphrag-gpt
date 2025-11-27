import win32com.client
import sys
import traceback

def try_methods(obj, method_names, *args, **kwargs):
    last_exc = None
    for name in method_names:
        meth = getattr(obj, name, None)
        if meth is None:
            continue
        try:
            return meth(*args, **kwargs)
        except Exception as e:
            last_exc = e
            continue
    methods_str = ", ".join(method_names)
    raise RuntimeError(f"Failed to call any of methods [{methods_str}] on {obj}. Last error: {last_exc}")

def try_attrs(obj, attr_names):
    for name in attr_names:
        if hasattr(obj, name):
            return getattr(obj, name)
    raise RuntimeError(f"None of attributes {attr_names} found on {obj}")

def get_xy_plane(part):
    # Try common ways to obtain the XY plane
    # 1) By name
    for method in ["GetDefaultPlane", "GetPlane", "PlaneByName", "GetPlaneByName"]:
        m = getattr(part, method, None)
        if m:
            try:
                plane = m("XY")
                if plane:
                    return plane
            except Exception:
                pass
    # 2) By dedicated XY getters
    for method in ["GetPlaneXY", "GetXYPlane"]:
        m = getattr(part, method, None)
        if m:
            try:
                plane = m()
                if plane:
                    return plane
            except Exception:
                pass
    # 3) From origin planes collection
    for attr in ["OriginPlanes", "GetOriginPlanes", "Planes"]:
        planes = getattr(part, attr, None)
        if planes:
            # Try index/name access patterns
            for key in ("XY", "xy", "PlaneXY", "XY_PLANE", 0):
                try:
                    plane = planes[key]
                    if plane:
                        return plane
                except Exception:
                    pass
            # Iterate and try to match by Name property
            try:
                for p in planes:
                    name = getattr(p, "Name", "")
                    if str(name).upper() in ("XY", "PLANE XY", "XY_PLANE"):
                        return p
            except Exception:
                pass
    raise RuntimeError("Failed to get XY plane from the part.")

def finish_sketch(sketch):
    # Try common methods to finish sketch editing
    for name in ["Close", "Finish", "EndEdit", "Deactivate", "ExitEdit"]:
        m = getattr(sketch, name, None)
        if m:
            try:
                return m()
            except Exception:
                pass
    return None

def get_profile_from_sketch(part, sketch):
    # Prefer sketch-native getters
    for name in ["GetProfile", "Profile", "CreateProfile", "BuildProfile"]:
        m = getattr(sketch, name, None)
        if m:
            try:
                prof = m()
                if prof:
                    return prof
            except Exception:
                pass
    # Fallback to part-level helpers
    for name in ["CreateProfileFromSketch", "GetProfileFromSketch", "MakeProfileFromSketch"]:
        m = getattr(part, name, None)
        if m:
            try:
                prof = m(sketch)
                if prof:
                    return prof
            except Exception:
                pass
    # As a last resort, some kernels accept the sketch object directly as a profile
    return sketch

def create_square_in_sketch(sketch, side_length):
    # Create a square centered at origin using a rectangle or a polyline
    half = side_length / 2.0
    x1, y1, x2, y2 = -half, -half, half, half

    # Prefer rectangle APIs
    for name in ["AddRectangle", "CreateRectangle", "DrawRectangle", "Rectangle"]:
        m = getattr(sketch, name, None)
        if m:
            try:
                rect = m(x1, y1, x2, y2)
                if rect:
                    return rect
            except Exception:
                pass

    # Fallback to polyline with closed loop
    pts = [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]
    for name in ["AddPolyline", "CreatePolyline", "DrawPolyline", "Polyline"]:
        m = getattr(sketch, name, None)
        if m:
            try:
                pl = m(pts)
                if pl:
                    return pl
            except Exception:
                pass

    # Fallback: add 4 lines
    def add_line(sk, p1, p2):
        for nm in ["AddLine", "CreateLine", "DrawLine", "Line"]:
            lm = getattr(sk, nm, None)
            if lm:
                try:
                    return lm(p1[0], p1[1], p2[0], p2[1])
                except Exception:
                    pass
        raise RuntimeError("Failed to add line segment to sketch.")
    l1 = add_line(sketch, (x1, y1), (x2, y1))
    l2 = add_line(sketch, (x2, y1), (x2, y2))
    l3 = add_line(sketch, (x2, y2), (x1, y2))
    l4 = add_line(sketch, (x1, y2), (x1, y1))
    return (l1, l2, l3, l4)

def create_pad_from_profile(part, profile, thickness):
    # Prefer part-level pad/extrude
    for name in ["CreatePad", "Pad", "Extrude", "CreateExtrusion", "AddPad", "AddExtrusion"]:
        m = getattr(part, name, None)
        if m:
            try:
                return m(profile, thickness)
            except Exception:
                pass
    # Try features container
    features = getattr(part, "Features", None)
    if features:
        for name in ["AddPad", "CreatePad", "AddExtrusion", "CreateExtrusion"]:
            m = getattr(features, name, None)
            if m:
                try:
                    return m(profile, thickness)
                except Exception:
                    pass
    raise RuntimeError("Failed to create pad/extrusion feature from profile.")

def update_part_and_doc(part, doc):
    for obj in (part, doc):
        if obj is None:
            continue
        for name in ["Update", "Rebuild", "Compute", "Refresh"]:
            m = getattr(obj, name, None)
            if m:
                try:
                    m()
                except Exception:
                    pass

def main():
    # Parameters (in millimeters)
    side_length = 100.0  # square side
    thickness = 10.0     # plate thickness
    plane_name = "XY"

    # Launch EvoShip
    evoship = win32com.client.DispatchEx("EvoShip.Application")
    try:
        # Show application if supported
        if hasattr(evoship, "Visible"):
            evoship.Visible = True
        elif hasattr(evoship, "Show"):
            evoship.Show()
    except Exception:
        pass

    # Create document and part
    doc = try_methods(evoship, ["Create3DDocument", "NewDocument3D", "CreateDocument3D"])
    part = try_methods(doc, ["GetPart", "Part", "GetActivePart"])

    # Ensure a main body if the API requires
    body = None
    for name in ["GetMainBody", "MainBody", "Body"]:
        try:
            body = getattr(part, name) if hasattr(part, name) else None
            if callable(body):
                body = body()
            if body:
                break
        except Exception:
            pass
    if body is None:
        # Try to create one
        for name in ["CreateBody", "AddBody"]:
            m = getattr(part, name, None)
            if m:
                try:
                    body = m("Body1")
                    break
                except Exception:
                    pass
    # Get XY plane
    try:
        plane = get_xy_plane(part)
    except Exception:
        # Last fallback: try by name directly if supported
        plane = try_methods(part, ["GetPlane", "GetDefaultPlane", "PlaneByName", "GetPlaneByName"], plane_name)

    # Create sketch on XY plane
    sketch = None
    for name in ["CreateSketch", "AddSketch", "StartSketch", "NewSketch", "SketchOnPlane"]:
        m = getattr(part, name, None)
        if m:
            try:
                sketch = m(plane)
                break
            except Exception:
                pass
    if sketch is None:
        # Some APIs create sketch from plane object
        sketch = try_methods(plane, ["CreateSketch", "AddSketch", "NewSketch"])

    # Draw square profile
    square_entity = create_square_in_sketch(sketch, side_length)

    # Finish sketch
    finish_sketch(sketch)

    # Build profile from sketch
    profile = get_profile_from_sketch(part, sketch)

    # Create pad (extrude) feature to thickness
    pad = create_pad_from_profile(part, profile, thickness)

    # Update model and document
    update_part_and_doc(part, doc)

    # Output some info for confirmation
    print("EvoShip square plate created successfully.")
    print(f"Side length: {side_length} mm, Thickness: {thickness} mm")
    if pad:
        name = getattr(pad, "Name", None)
        print(f"Feature: {name if name else 'Pad/Extrude'}")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("Error while creating square plate:", e)
        traceback.print_exc()
        sys.exit(1)