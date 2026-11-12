# Town landing pages: /areas-we-serve/<slug>/
# Each town gets its own intro, route, and local notes so the pages are not copies of each other.
# These are the redirect targets for the old Auto Addict Car Care town repair pages.

TOWNS = {
 "framingham": dict(
    name="Framingham",
    drive="about 20 minutes",
    route="Take Route 9 west or Route 20 west toward Marlborough, or hop on I-495 north from Route 9.",
    nearby=["Natick", "Ashland", "Sudbury", "Southborough"],
    intro="Framingham has no shortage of dealerships on Route 9, and plenty of BMW, Audi and VW owners there are looking for something better: dealer-level diagnostics and parts without the dealer markup or the week-long wait. That's what we built Auto Addict Works to be.",
    local=[
      "Daily commuters on Route 9 and the Mass Pike, like the 3 Series, X3, X5, Audi Q5 and A4, VW Atlas and Tiguan, are what we work on every day.",
      "Stop-and-go Route 9 traffic is hard on brakes, cooling systems and turbo engines, and those are the jobs we see most often.",
      "If you're between dealer service visits or your car is out of warranty, we can pick up your maintenance schedule where the dealer left off.",
    ],
    faq_extra=("Is it worth driving from Framingham instead of using a closer dealer?",
               "For most European cars, yes. You get factory-level diagnostics (BMW ISTA), genuine and OE parts, and a written estimate before any work starts, usually for less than dealer labor rates. Many Framingham customers combine drop-off with their commute toward I-495."),
 ),
 "hopkinton": dict(
    name="Hopkinton",
    drive="about 15 to 20 minutes",
    route="Take I-495 north to the Marlborough exits, or come up Route 85 through Southborough.",
    nearby=["Southborough", "Ashland", "Westborough", "Holliston"],
    intro="Hopkinton drivers put serious miles on their cars between I-495, the Pike and back roads. When a BMW, Audi or VW starts throwing warning lights, you want a specialist close by who works on these cars every day, not a general shop guessing at codes.",
    local=[
      "Larger family and all-wheel-drive cars, like the BMW X5 and X7, Audi Q7, VW Atlas and Mercedes GLE, are a big part of what we service.",
      "AWD systems, transfer cases and suspension wear are common on these, and we have the factory procedures and parts access to do them right.",
      "Winter salt and back-road driving add up, so we check brakes, suspension and underbody on every visit.",
    ],
    faq_extra=("Do you work on all-wheel-drive and xDrive systems?",
               "Yes. We service BMW xDrive, Audi quattro and VW 4MOTION systems, including transfer case fluid service, diagnosis and repair."),
 ),
 "hudson": dict(
    name="Hudson",
    drive="about 10 minutes",
    route="Take Route 85 south into Marlborough. We're a short hop from downtown Hudson.",
    nearby=["Marlborough", "Stow", "Berlin", "Bolton"],
    intro="Hudson is right next door, which makes us the closest European specialist for a lot of Hudson BMW, Audi and VW owners. Drop the car on your way to work and we'll call with a written estimate before anything gets touched.",
    local=[
      "Being 10 minutes away makes routine maintenance easy: oil service, brakes and inspections without a trip to a dealer.",
      "We work on everything from daily-driver 3 Series and VW GTIs to weekend M cars.",
      "For bigger jobs like timing chains, oil leaks or cooling systems, we explain what we found with photos before you approve the work.",
    ],
    faq_extra=("How close is Auto Addict Works to Hudson?",
               "About 10 minutes down Route 85 into Marlborough. We're at 41 Brigham Street, Unit 1."),
 ),
 "southborough": dict(
    name="Southborough",
    drive="about 10 minutes",
    route="Come north on Route 85 into Marlborough, or take I-495 one exit north.",
    nearby=["Marlborough", "Westborough", "Framingham", "Hopkinton"],
    intro="Southborough borders Marlborough, so we're one of the closest European specialists to town. BMW, Audi, VW and Mercedes owners in Southborough get dealer-level diagnostics and genuine parts without driving to a dealership.",
    local=[
      "If your European car is just out of warranty, we can pick up its maintenance with the same factory procedures the dealer uses.",
      "We use BMW ISTA factory diagnostics and follow factory service procedures, so your service history stays complete.",
      "We also do coding and retrofits, like enabling features or adding CarPlay.",
    ],
    faq_extra=("Will servicing my car with you affect my warranty?",
               "No. You're free to use an independent shop for maintenance. We use genuine or OE-supplier parts and document every visit, so your records stay in order."),
 ),
 "westborough": dict(
    name="Westborough",
    drive="about 15 minutes",
    route="Take I-495 north to the Marlborough exits, or Route 9 east to I-495 north.",
    nearby=["Northborough", "Southborough", "Shrewsbury", "Hopkinton"],
    intro="Westborough sits right at the I-495 and Route 9 crossroads, a quick run up 495 to our Marlborough shop. If your BMW, Audi or VW needs more than a quick-lube place can handle, we're the specialists down the road.",
    local=[
      "High-mileage highway commuting on I-495 and I-90 tends to show up as oil leaks, cooling system wear and suspension work.",
      "We diagnose before we replace anything, so you pay for the actual fix, not a pile of guessed parts.",
      "Prefer to plan ahead? Ask us to put together a maintenance plan for your mileage and model.",
    ],
    faq_extra=("Can you diagnose a check engine light the same day?",
               "Usually, yes. We scan with factory-level tools, explain what we found, and give you a written estimate before any repair. Call ahead and we'll tell you the earliest opening."),
 ),
 "worcester": dict(
    name="Worcester",
    drive="about 25 to 30 minutes",
    route="Take I-290 east to I-495 north, then the Marlborough exits.",
    nearby=["Shrewsbury", "Northborough", "Westborough", "Boylston"],
    intro="If your BMW, Audi or VW needs a specialist rather than a general repair shop, we're about 25 minutes from Worcester via I-290. Factory-level diagnostics and a team that works on these cars every day are worth the drive.",
    local=[
      "For problems a general shop couldn't solve, like intermittent warning lights, electrical faults or repeat failures, we start with factory diagnostics instead of guesswork.",
      "Bought a used BMW, Audi or VW with an unknown service history? We do pre-purchase inspections and catch-up maintenance plans.",
      "Planning a performance build? See our build planner and past builds.",
    ],
    faq_extra=("Is it worth driving from Worcester to a European specialist?",
               "If a general shop has already had a go at it, or you want it done right the first time, yes. You get factory-level diagnostics, genuine and OE parts, and a written estimate before any work starts."),
 ),
}
