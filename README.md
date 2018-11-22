# Real-time matching cuts in parts in factory pipeline.
This is a commercial project I have done in YOUEdata. We design a real-time algorithm to match  cuts  for certain type parts in a pipeline.

The samples of the cuts are human-made from photographs.

We use the Matchtemplate algorithm in OpenCV to find possible matchings.

The issue with MatchTemplate is that the algorithm returns five best matchings, however the matching with highest score is not always 
the desired matching because of camera glitching or noise. 

The solution to this problem is to use a majority vote. 

We samples from the camera for 5 frame for a second in a 30fps stream
and we keep the 5x5x5 mathcing results in a vector and counting how many times a mathcing appeared in the vector.

Then the algorithm output the matching appeared most in last five second. 





