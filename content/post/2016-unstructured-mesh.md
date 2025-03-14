+++
date = "2016-03-25T15:50:58+02:00"
short_text = ""
title = "Interpolating Bathymetry To Unstructured Mesh"
[[authors]]
    name = "Thomas Bryce Kelly"
    id = "Thomas Bryce Kelly"
    is_member = true
+++

A few weeks (perhaps months) ago I introduced the side project that I am involved with whereby our aim is to develop a hydrographic model for Apalachicola Bay, Fl. Today I wanted to provide an update for that project while also sharing some interesting problems that we’ve had to work around.

![](/2016-unstructured-mesh/figure1.png)

The last we spoke, we had decided on using FVCOM to model the bay and surrounding waters. Our choice was contingent on having a model that could accurately describe the complex coastline and relatively flat and shallow water column. FVCOM uses an unstructured mesh, meaning that instead of using a grid with a regular pattern (think Manhattan’s streets and avenues), the model domain is instead more freeform (think rural street map). This offered both the possibility for improved spatial resolution and an opportunity for use all to gain proficiency in a new skill.

![](/2016-unstructured-mesh/figure2.png)
An example of a curvilinear grid developed for a model by Huang et al. (2002).

![](/2016-unstructured-mesh/figure3.png)
An example of an unstructurd grid that we developed for FVCOM.
 

A unstructured grid like this is defined as a set of points or nodes and the connections between them (i.e. who is connected to who).

From this point, the next step in forming the final model domain is to add depth data to the mesh. We need to be able to assign a depth for each node forming the mesh since the model will then be able to define the 3 dimension fluid parcels that makes it a hydrodynamic model.

Thanks to the powers of the internet and the USGS, we have bathymetric data for the entire region with various levels of detail (from 30m to as coarse as 100m).

![](/2016-unstructured-mesh/figure4.png)
Coarse resolution (~100m), topographic data including the entire region and land.

![](/2016-unstructured-mesh/figure5.png)
The high-resolution (30m) bathymetric data encompassing just the bay.

The challenge comes in using these gridded data products for an unstructured mesh like ours (aka square peg and round hole). This is the data-informatic side of things that I enjoy, so let’s get into it.

The obvious answer would be to take some kind of nearest-neighbor type approach whereby the value of one of our nodes is simply the depth value of the closest grid point in the bathymetric data we have. For most applications this would probably be a great route to take since it is simple to implement and it makes no-assumptions about the topography that there (more on this later). But, the result would be ‘wrong’.

While I don’t mean ‘wrong’ in a pejorative sense, it is merely that the depth values generated would not be the values that we would measure unless out point and the data point were coincident. Ultimately it is a bad estimate given the wealth of data available.

So, what direction should we take? Let’s start by defining our assumptions:

Submarine topography is generally smooth (at least in Florida where topographic relief is low and karst underlayment).
The USGS data is great, but the accuracy of the data and the subsequent project of the data should not be considered infallible. Consider that even if the data is perfect, the accuracy of the coordinates (least significant digit) and depth compounded by the uncertainty of our modeled coastline and nodal points means that the resulting project of the data is likely to be imperfect.
Accuracy of location is not as important as accuracy of the large-scale contours due to the dissipation of the small scale as you move away from the coast and into the flat open bay.
Taken together, these give us a footing on which to build an interpolation scheme.

Given that the topography is assumed smooth and inaccurate, let’s start by thinking about averaging across some number of points (e.g. a classic interpolation scheme)[1]. using n points, we arrive at this simple average:

$$d=\frac{1}{n}\sum{d_i}$$

where $d_i$ is the depth at the ith closest point.

Okay, while this is a possible answer, we’re ignoring all of the position/distance data we have. Since we know where the node is and all the bathymetric points around it, we can take a spatial mean instead.

For a spatial mean, we calculate some weighting value, $w_i$, that allows us to control the relative contribution of each depth to the final, estimated average.

$$d = \frac{1}{\sum{w_i}}\sum{w_i\cdot d_i}$$

The question now is to decide how we should weight the values. We could let the weight of a value decline linearly with distance; for example, let the weight decrease by 1% for every meter away it is:

$$w(distance) = 1-0.01\cdot distance$$

But that seems rather arbitrary. Why 1%? Why per meter?

Instead perhaps we should work in the natural units of the problem. We can weight them according to the reciprocal of the distance. here we’ll use whatever the natural units for distance actually are. Here they’re meters whereas in another model they could be cm or km with no difference[2].

$$w(distance) = \frac{1}{distance}$$

So let’s take a look at the implementation of this idea. To begin with we first have to find the nth closest points, that’s the j loop. After that then we can calculate the new depth and save it in depths. Rinse and repeat for all nodes.

    depths = zeros(length(p(:,1)),1);
    n = 2;

    h = waitbar(0,'Starting...');
    count = 0;
    len = length(p(:,1));
    step = floor(len/100);

    for i=1:length(p(:,1))
        sub = sqrt( (data(:,1)-p(i,1)).^2 + (data(:,2)-p(i,2)).^2 );
        points = zeros(n,3);
        
        tempData = data;
        % Loop to select closest points
        for j=1:n
            [m1,m2] = min(sub);     % Find closets point
            points(j,:) = tempData(m2,:);     % save point
            sub(m2) = [];           % Remove point from list to find next smallest
            tempData(m2,:) = [];
            
        end
        
        % Weight of reciprocal distance
        w = 1 ./ sqrt((points(:,1)-p(i,1)).^2 + (points(:,2)-p(i,2)).^2 );
        
        depths(i) = sum( w .* points(:,3) ) / sum(w);
    
        if mod(i, step) == 0
            count = count+1;
            waitbar(count/100, h, sprintf('Progress: %d%%',count));
        end
    end

    close(h);

    %% Plot the results
    figure(1)
    stem3(p(:,1), p(:,2), depths,'.');
    
While this implementation is not very efficient (it takes a while for 60,000 nodes…), it is transparent and that is the first priority if you’re goal is code-reuse. One of the goals we have is that all of the scripts generated for this project should be code that can be used for future projects. Performance is only requisite for the final model (when it makes a real difference).

If we didn’t assume that the topography was smooth or if we had absolute faith in the accuracy of the points we could fit curves to the bathymetric data instead. For example, assuming perfect accuracy of the data, we could calculate the local gradients and use them and a cubic spline between the two closest points to arrive at an estimated value for the depth. There are many non-averaging techniques that could be used instead.
By no difference, I mean in terms of the code. Here we’re making the assumption that the units being used prior to our code are the units ‘appropriate’ to the problem at hand.