#!/bin/python
sfmaplow={
    "2016":{"nominal":0.63,"scaleUp":0.74,"scaleDown":0.52},
    "2017":{"nominal":1.00,"scaleUp":1.11,"scaleDown":0.89},
    "2018":{"nominal":0.94,"scaleUp":1.02,"scaleDown":0.86}
}


sfmaphigh={
    "2016":{"nominal":0.92,"scaleUp":0.88,"scaleDown":0.96},
    "2017":{"nominal":0.82,"scaleUp":0.78,"scaleDown":0.86},
    "2018":{"nominal":0.78,"scaleUp":0.74,"scaleDown":0.82}
}

print sfmaplow["2016"]["nominal"]
print sfmaplow["2018"]["scaleDown"]
