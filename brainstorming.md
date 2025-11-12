# Technical Room Optimization

## Questions/Brainstorming

### What are the different ways we can optimize the configuration?

- Space
- Expandability (future)
- Accessibility
- Maintainability
- Shortest distance between connections (ease of connection)
- Efficiency

### Is there a dataset that I can use to understand the current state of room size vs building size?

### What are some external variables that are likely to affect the size of the room?

- _Building Location_
  - Is it next to other buildings?
  - What are the weather conditions like in that location?

- What is the maximum capacity that the building is expected to handle?
- Do we design around the max capacity or do we design around the average case?

### Does the type of building affect the size of the room needed?

- Is this building for commercial use?
- Is this building a residential building?
- Is it mixed use

### Does the location of the building affect t

## Assumptions

- After rereading the task questions, it seems like we are not trying to design the the equipment room from end to end. But it seems that we are given a list of equipment types that we would like to fit, in the equipment room. This means that my previous questions, and ideas about the type of building, location, load etc.. can be discarded, since we can make the assumption that we are given the components before hand.

- Let's assume we are developing for your average London building, and not some kind of outlier project like Burj Khalifa.

- Another assumption we can make is that we are given the components before hand, along with their operational restrictions.

### Ramblings

We may have different criteria.
We know that the size of the room is directly proportional to the size of the building.

What I would like to achieve is a model that allows me to tweak the parameters when coming up with the layout.

Can we have multiple formulas that model optimization criteria?

For example (these are just EXAMPLES):

- ease of installation/maintainibility = accessibility / distance-between connections
- expandability = (total-space-left \* nomalized_accesiblity)
- efficiency = normalized-distance-between-hot-and-cold / (normalized-distance-between-components-that-need-to-be-hot + normalzied-distance-between-components-that-need-to-be-cold)
- Path simplicity score. Just because a path can be made, doesn't mean it should.
  - A path should be easy to build in the physical world
  - should not zig/zag too much -> this may actually affect the physical system (pressure, heat, surface area of path etc...)

We also need to consider the overlapping parts, this is an optimization function and we have to come up with the cost function.

- How does the placement of a specific piece of equipment affect our criteria
- How are current designs graded?
- Are there existing functions in the field of engineering that calculate them?
- Can this be modeled as an RL problem?
- If we have existing functions, can we use some modeling to simulate how a configuration would behave. For example, there are functions that we use to design models, based on sane engineering principles. But there are things that don't make sense for use to model as we focus on larger things. For example, the efficiency formula mentioned earlier, we can also consider the distance between connections as heat loss or heat gain were it matters, and understand how the whole system reacts. The hard part is finding the best configuration. This really really seems like an RL problem... but that is just my intuition..

We need to have hard-coded stops as well, for example it should not be possible to have a distance less than the regs specify, or more than the room dimensions would allow.

We need to take into account real world physical constraints.

Upon further inspection, it looks like the 3d model is trying to hint something to us:

- We don't just need to account for connection distances, but connections are phyisical this means they have diameters, and take up volume as well. So just like we need to consider for accessibility, that we need a clear path from entrance to device we also need to consider, that different devices need to connect to each other.
- Should we consider total volume of the connection as part of the metrics instead of length of the connection?
- Should we consider types of connections? Electrical, vs Ducts, vs pipes, how do we factor them into the ease of installation/maintainibility.

I am starting to realize that I need to expand/refresh my vocabulary:

- Adjacent:
  In geometry, "adjacent" refers to two figures that share a common boundary or edge without overlapping. For example, two squares that share a side are considered adjacent.
- Orthoginal:

## Constraints

- All the equipment fits.
- All connections that need to be made can be made
- Equipment cannot overlap
- There needs to be a path to reach the equipment
- Different types of equipment may need more or less:
  - clearance
  - path to equipment may need minimum Width/Height

- Pipes and ducts have a certain region, for them to be placed in 3d space
  - You wouldn't place pipes on the floor, even though it is technically a valid path- The equipment needs to be on the ground it cannot hover
  - What are the physical design constraints that help us understand if a path can be made?
  - for example if we want to turn or change direction, we can do so only in 90 degree bends, as that is a limitation of pipe design, we do not have curved pipes.
  - What if we also limit the number of bends we can make when we are path finding? So we are constrained by the pressure/head or any other loss for given path
  - Different equipment/path types, can be given different maintainibility/accessibility scores, depending on how often we expect to maintain them. We can even have a minimmum normalized maintainiblity score for each equipment/path type. While our algorithm is generatively traversing the different equipment/path combinations, if we do not meet the min criteria then path is dropped/backtracked etc...
  - Prefer Manhattan routing, a technique used in circuit designs where connections are created in a grid like pattern, resembling the streets of manhatten new york. (we should still allow for diagonal, but in a constrained way, so for example, slope of the diagonal, and we can heavily limit number of allowed diagonal paths. Based on the image provided in the problem spec, it seems that
  - We also are constrained by the actual pipes/ducts available to us during the design. for example to route waste pipe paths, we provide a list of components that, we can patch together, path = straight pipe(max len=3m) + connection joint (this matters more in ducts) + straight pipe (len =1.5m), 90 degree bend pipe (we can have different types of 90 degree bend pipes, with varying harshness of bends, for example the model can decide if it is worth having a harsh bend that prioritizes space savings, over a a more gradual bend that may take more space but be more efficient.) This becomes useful because now that we have constrained the model, with the type of paths it can make we have reduced the search space even further. and again, this will allow us to backtrack at earlier stages just like the minimum maintainability idea we mentioned above. But instead of just maintainability, the criteria can be space, or even lack of availability of a specific path componenent to be able to reach the end of the path, or even having too much loss/head for a given path design, etc...
  - This also brings me to another constraint, just like we have the idea of path types that we can connect together, we also have different parts of the path that have different criteria, for example if we have a valve (wheel turning), on a specific part of the path then it may have a higher accessibility/clearance score, with a minimum score that has to be respected.
  - We may even need to create paths to reach certain parts of other paths, we can call those accessibility paths, those accessibility paths need to be modeled in a way were if an accessibility path exists next to an unreachable component, then the component becomes accessible. So we need a way were we allow for an (impossible unnaccessbile) path to be created, and even allow for multiple impossible paths to be created then try to create accessibility paths for them if needed. If possible proceed, if not then we may have to backtrack. Should the accessibility paths be created before or after? Accessibility paths can be thought of as ladders used to get to certain places that have a high accessibility/maintainibility score.
  - We should also consider during the equipment configuration stage, that some equipments may require to be placed on a specific platform type, so just like we have path types, we can also have platform types, vibration platform, concrete base etc...

## Scoring Functions and validation

In order to come to come up with effective optimization algorithms, it is important to be able to understand how we can compare 2 different equipment/path configurations with each other. I can try and come up with some scoring functions based on raw intuition, but it would be more helpful if I could rely on existing ways a system is measures:

- Compare using intuitive metrics from my previous ramblings

- What about using engineering metrics such as cooling efficiency, or pressure drops/ head loss, energy consumption etc..

- What if come up with a complexity metric that penalizes complex designs.

- But most importanty we need a baseline,

- What is a complex design

- What is a good design

- We need to find existing equipment and path configurations that the industry considers the gold standard, and battle test our scoring criteria based on them

- The scoring criteria needs to be normalized such that it is scoring the design and not the size of the project.

- To determine if we have a valid scoring function we would expect that 2 gold standard designs will have a similar score.

- We can also look at poorly designed systems and do the same, and we would also expect 2 poorly designed systems to score the similarly.

- We should also check to see if our scoring function can capture decent designs, can our scoring function exhibit nuance? We would do that by finding designs patterns that used to be considered gold, but have now been shelved because better patterns/standards have been discovered, so they are not bad, but there is better now. Maybe if we look at the history of equipment room design we can determine how we discovered better designs over time, and use that to capture in-between scores? To verify we would want our scoring function to score higher on the modern standards.

- One more thing to do, is we need to validate our scoring criteria, iteratively as well. So let's assume we went through all the stages, and we designed a model that can stick the constraints, and develop a valid equipment configuration criteria, and a valid path criteria. We need to visually compare it to a given optimal design that we already know about. If our we scored highly despite it being visually unnacceptable, or implausable compared to the ideal one, then somehow our model is gaming the scoring function and we need to update the scoring function accordingly. Not sure how to put this in more concrete terms, using visual here seems a bit lofty, but I think you get the point.

## Algorithmic Designs

- _Path Finding_
- Path Validation
  - Can a path be made, does it overlap with existing paths
  - Just because a path can be made, the question becomes should it be made?
  - We need to take into account that these are physical systems that are going to be built, so sometimes, grouping related paths with each other makes sense, this makes for a system that is easier to reason about and maintain, (think of convoluted AI code that works, vs deliberate intentional simple code that also works as an analogy)
  - If we decide to constrain paths to grids, then does that simplify the problem?
  - If we do contrain to grids we need to make sure that we do not have zig/zaggy path
  - Types of weird paths we may encounter:
    - zigzag due to trying to create a diagonal path
    - zigzag due to trying to finding a "valid path", but not an optimal one

- _Path Optimization_
  - Once objects are placed we need to start making connections
  - Place the first connection, then second etc..
  - How do we decide the order of connection placement? (maybe largest surface get's priority for connecting?) then smaller and smaller.
  - How do we grade a path?
  - Even paths need to be accessible, but we score accessibility differently based on the type. Now that I mention it, I should probably create path types just like we have volume types, and dependding on the type, they also may need to be accessible or not, and the definition of accessibility also varies here. Accessing a duct, or waste pipe is different than accessing the actual equipment.
  - Do we have different types of paths?
    - Movement paths -> paths used to get from entrance to equipment
    - Duct paths, waste paths, etc...
    - Movement paths do not need accessibility as they are the ones measuring the accesibility?
    - Maybe make a distinction between paths and connections? with are paths?
    - Maybe I am thinking of negative space paths vs positive space paths, if I were to think in terms of abstractions, hmmm

- Equipment Configuration Validation
  - path space -> the complete set of possible paths we can have for a given equipment placement configuration
  - path configuration -> a complete set of paths, that connects all the equipment to where they need to be connected
  - equipment configuration -> a configuration that allows us to place all the equipment in a way that respects our constraints
  - how do we determine if an equipment configuration is a valid configuration?
  - a valid configuration needs to respect all the constraints but also needs to allow us to make all the connections to have a valid path configuration
  - maybe the first step is to determine if we have a valid configuration or not, given a configuration.

- Equipment Configuration Optimization
  - We know that equipment placement affects the our path space
  - The order in which we place our paths affects the rest of the potential paths but not the space itself.
  - If pathspace is the set of all possible paths, given an equipment configuration, then what do we call the rest of the subspace for the rest of the paths, given a path configuration?
  - Equipment Configuration -> Path-Space{Path configuration 1, Path conf2, path confn }
  - Can we think of our path space as a tree? Where if we decide to place a path for a specific piece of equipment in a specific position, then we effectively reduce our path-space, we take a branch of our tree. The question then becomes how do we find the optimal branch?
  - This seems like a tree traversal problem, let's go back to how we would design something in 3d space, this thinking exercise will help me determine some constraints that I can use to determine whether a tree branch is a valid branch, or whether I should simply drop that branch.
  - I would cluster related equipment with each other. I would also cluster related paths with each other, I would eliminate difficult paths, to reduce our potential pathspace using our path validation/optimization criteria. I would follow a set of rules that industry agrees on, I would start by fitting the largest paths first. Since we mentioned that ideally we would want related paths togethor, can we treat a group/cluster of small paths that originate from a common direction as a larger path? This can also simplify our problem space, and eliminate weird configurations
  - If different configurations result in different path spaces, then how do we find the equipment configuration that will result in the optimal path configuration

- Equipment placement
  - path space -> the complete set of possible paths we can have for a given equipment placement configuration
  - We know that equipment placement affects the our path space
  - The order in which we place our paths affects the rest of the potential paths but not the space itself.
  - If pathspace is the set of all possible paths, given an equipment configuration, then what do we call the rest of the subspace for the rest of the paths, given a path configuration?
  - Equipment Configuration -> Path-Space{Path configuration 1, Path conf2, path confn }
  - Certain equipment need to be faced in a certain orientation, also we may have equipments with clear edges vs equipment that is edgeless, like water tanks for example
  - We can constrain equipment rotation for edged quipment to have 90 deg rotations, and we can give more flexibility to edgless equipment

## Data Models

### Ramblings

- other points this point connects to
  - should we add a constraint in terms of how points are modelled?
  - should we assume that a point should be connected to 3 other points for it to be a valid connection?
  - should we make a distinction between 2d points and 3d points?
  - what is the simplest version of a point?
    - A 2d point, must have x,y
    - Must be connected to only 2 other points
    - We can make it simpler by adding an adjacency restriction
    - The adjacency restriction is useful for paths as well, since a path is going to be made up of points
    - I think I mixed up points and paths.

### High Level Models Proposed

- 2D Point
  - x
  - y

- 3D Point
  - x
  - y
  - z

- 2D Plane

- 3D Surface -> overkill but just writing it down anyways.

- Volume (Is composed of points or planes?)

- Room (Inherits from volume)
  - Layout
    - Points or planes?

- Access Points (Inherits from 2D Plane)
  - Width
  - Height
  - Coordinates

- 3D Paths Inherits from Volume

- Equipment (Inherits from volume)
  - Connection (In/Out) (Inherits from 2D plane)
  - Constraints

## Putting it together

- We need to identify the constraints
- We need to design the scoring functions/criteria
- We need to decide on a validation strategy based on the scoring criteria
- We need to design a data interfaces/models that represent our real world room/equipment, paths etc...
- We need to design algorithms that based on those models, and then use the scoring function/criteria/validation strategy to measure effectiveness
- Finally we need to iterate iterate iterate. iterate on the scoring functions, iterate on the validation strategy, improve our system representatio overtime, maybe first we start with blocks and cubes, and grid-layouts, then we move to more finegrained representation that allows for more creativity for the path movement etc... improve the algorithms etc...
