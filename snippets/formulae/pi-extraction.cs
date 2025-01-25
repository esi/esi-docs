int[] CalculateExtractorValues() {

    //Inputs - these are set from the API results.
    //Note that all times are in seconds.
    int duration = 171000; //1d 23h 30m; from API expiryTime-installTime
    int cycleTime = 30 * 60; //30 minutes, value from API cycleTime * 60
    int quantityPerCycle = 6965;

    //These constants are the defaults in dgmAttributeTypes. They may change.   
    const float decayFactor = 0.012f; //Dogma attribute 1683 for this pin typeID
    const float noiseFactor = 0.8f;   //Dogma attribute 1687 for this pin typeID
           
    int numIterations = duration / cycleTime;
    float barWidth = cycleTime / 900f;
    int[] values = new int[numIterations];

    for (int i = 0; i < numIterations; i++) {
        float t = (i + 0.5f)*barWidth;
        float decayValue = quantityPerCycle/(1 + t * decayFactor);
        double phaseShift = Math.Pow(quantityPerCycle, 0.7f);
        
        double sinA = Math.Cos(phaseShift + t * (1/12f));
        double sinB = Math.Cos(phaseShift / 2 + t * 0.2f);
        double sinC = Math.Cos(t * 0.5f);
   
        double sinStuff = Math.Max((sinA + sinB + sinC) / 3, 0);
   
        double barHeight = decayValue * (1 + noiseFactor * sinStuff);
        values[i] = (int) (barWidth * barHeight);
   }
   return values;
}
