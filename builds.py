"""Builds showcase data. Page goes live once there are at least two builds.
Rules: no tuner names (tuning credited to an independent specialist), plates blurred,
owner OK required for customer cars. Sections with no data are hidden on the page."""

BUILDS = [
  dict(
    slug="project-1300",
    name="Project 1300",
    tag="Shop car",
    car="2017 BMW 340i xDrive (F30)",
    engine="B58 Gen 1",
    color="Satin black wrap",
    power="1,300 hp", power_note="on E85",
    fuel="E85 (flex fuel)",
    trans="Built 8-speed automatic",
    use="Drag",
    story="Our own 340i, built in this shop with the same process we use on customer cars: health check first, fueling before boost, and a drivetrain that can hold the power.",
    mods={
      "Power": ["Turbosmart 76mm turbo", "RK Autowerks intake manifold"],
      "Engine": ["Built engine"],
      "Fueling": ["Upgraded low-pressure fuel pump", "Upgraded injectors", "Return-style fuel system",
                  "Port injection", "Reflex+ controller", "Flex fuel (E85)"],
      "Drivetrain": ["Built transmission"],
      "Chassis": ["Coilovers", "Drag radials"],
      "Exterior": ["Satin black wrap by Auto Addict Car Care"],
    },
    tuning="Custom flex fuel calibration by an independent tuning specialist.",
    images=dict(card="/img/builds/project-1300-card.jpg", hero="/img/builds/project-1300-hero.jpg",
                og="/img/builds/project-1300-og.jpg"),
    gallery=[], timeline=[], dyno=None,
    builder_link="#p=b58f&m=drag&hp=1300",
  ),
  dict(
    slug="m2-72mm",
    name="M2 72mm",  # placeholder title, confirm
    tag="Customer build",
    car="2025 BMW M2 (G87)",
    engine="S58",
    color=None,
    power=None, power_note=None,   # NEED: power figure and fuel
    fuel=None, trans=None, use=None,  # NEED: trans (manual/auto, built?), use
    story=None,
    mods={
      "Power": ["Precision 72mm single turbo", "Hood dump"],
      "Engine": ["Cam lock"],  # confirm meaning
      "Chassis": ["Beadlock wheels"],
      # NEED: confirm which of the 340i's mods carry over (built engine, built trans, fuel system, port injection, Reflex+, flex fuel, coilovers, drag radials)
    },
    tuning="Custom calibration by an independent tuning specialist.",
    images=dict(card="/img/builds/m2-72mm-card.jpg", hero="/img/builds/m2-72mm-hero.jpg", og="/img/builds/m2-72mm-og.jpg"),
    gallery=[], timeline=[], dyno=None,
    owner_ok=False,  # NEED before publishing
    builder_link="#p=s58&m=drag",
  ),
]
