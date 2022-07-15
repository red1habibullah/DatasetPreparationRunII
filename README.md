# DatasetPreparationRunII
Each channel has a separate script and for each channel there is running od Data, SignalMC, with fakeSystematics,tauScaleSystematics oR JEC Systematics.

For each scripts, one needs to change the following directories to make the code work:

```bash
fakebaseDir='/afs/cern.ch/user/r/rhabibul/DatasetPrepRunII_Boosted/CMSSW_10_2_13/src/DatasetPreparationRunII/data/
```
The input directories will remain the same and the outpur directories dould either remain the same or one can modify them to write to their owen directories. Note the RooDataset names carry a name convention which has been agreed upon and followed for the last several 
months.

