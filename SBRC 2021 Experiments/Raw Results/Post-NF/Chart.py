import sys
import numpy
import matplotlib
import matplotlib.pyplot as plot
from matplotlib import colors as mcolors
import matplotlib.patches as mpatches


matplotlib.rcParams.update({'font.size': 10})
matplotlib.rc('axes', labelsize=12)

def autoLabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = round(rect.get_height())
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight="bold")

def createIntervals(filesData, xStep, xRange):

	intervalResults = [[] for processFile in filesData]

	for xIndex in range(1, int(xRange / xStep) + 1):
		xInit = xStep * (xIndex - 1)
		xEnd = xStep * xIndex

		for fIndex in range(len(filesData)):
			intervalResults[fIndex].append(0)
			for timeResult in filesData[fIndex][2][2]:
				if timeResult >= xInit and timeResult < xEnd:
					intervalResults[fIndex][-1] += 1

	return intervalResults

def createCDFIntervals(intervalData, cumulativeReference):

	return [numpy.cumsum([data/cumulativeReference for data in particularIntervals]) for particularIntervals in intervalData]

def makeBar(filesData):

	labels = ["COO", "Leaf", "COVEN (HTTP)", "COVEN (Socket)"]
	textures = ['\\', '|', '+', 'O', '/', '-', 'x', '.']
	noems = [data[2][0][0] for data in filesData if not data[0].endswith("EMS")]
	noems_err = [data[2][1][0] for data in filesData if not data[0].endswith("EMS")]
	ems = [data[2][0][0] for data in filesData if data[0].endswith("EMS")]
	ems_err = [data[2][1][0] for data in filesData if data[0].endswith("EMS")]
	x = numpy.arange(len(labels))
	width = 0.35

	fig, ax = plot.subplots()
	rects1 = ax.bar(x - width/2, noems, width, label='Sem EMS', facecolor="#AFAFAF", yerr = noems_err, ecolor="black", error_kw={"lw": 1, "capsize":3})
	rects2 = ax.bar(x + width/2, ems, width, label='Com EMS', facecolor="#626262", yerr = ems_err, ecolor="black", error_kw={"lw": 1, "capsize":3})

	for index in range(len(ax.patches)):
		ax.patches[index].set_hatch(textures[index])

	ax.set_ylabel('Tempo (ms)')
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	plot.legend(loc = 2, handles = [mpatches.Patch(label="Sem EMS", facecolor="#AFAFAF"), mpatches.Patch(label="Com EMS", facecolor="#626262")])

	autoLabel(rects1, ax)
	autoLabel(rects2, ax)

	fig.tight_layout()
	plot.show()

def makeHistogram(intervalData, xRange, barLabels):

	step = int(xRange/len(intervalData[0]))
	x = numpy.arange(0, xRange, step)
	
	fig, axis = plot.subplots()
	fig.subplots_adjust(left=0.15, bottom=0.15, right=0.99, top=1, wspace=0, hspace=0)
	axis.grid(True,linestyle='--',axis='y')
	
	textures = ['\\\\', '//', '||', '--', '++', 'xx', 'OO', '..']
	colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7']
	for xi, coo, cooems, leaf, leafems, chttp, chttpems, csock, csockems in zip(x, intervalData[0], intervalData[1], intervalData[2], intervalData[3], intervalData[4], intervalData[5], intervalData[6], intervalData[7]):
		for i, (h, c, t) in enumerate(sorted(zip([coo, cooems, leaf, leafems, chttp, chttpems, csock, csockems], colors, textures))):
			if h == 0:
				continue
			axis.bar(xi, h, color=c, hatch=t, width=step/1.2, zorder=-i)

	axis.set_xlabel("Tempo (ms)")
	axis.set_ylabel("Execuções")
	#plot.xticks([0,100,200,300,400,500])
	plot.legend(handles=[mpatches.Patch(label=barLabels[i], hatch=textures[i], edgecolor="black", facecolor=colors[i]) for i in range(len(barLabels))])
	plot.show()

def makeCDF(cdfData, xRange, barLabels):
	
	step = int(xRange/len(cdfData[0]))
	x  = numpy.arange(0, xRange, step)
	lineStyles = ["-", "-", "--", "--", "-.", "-.", ":", ":"]
	colorStyles = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'] #["#FF0000", "#FF8282", "#018924", "#81FAA0", "#D18200", "#F9CB80", "#970101", "#FD8787"]

	for index in range(len(cdfData)):
		plot.plot(x, cdfData[index], label=barLabels[index], linestyle=lineStyles[index], color=colorStyles[index])
	
	plot.xlabel("Tempo (ms)")
	plot.ylabel("Probabilidade")
	plot.legend(ncol = 3, bbox_to_anchor=(1.1, -0.15))
	plot.show()

processFiles = [["COO", "Post-NF-COO-Direct.csv"], ["COO + EMS", "Post-NF-COO-EMS.csv"], ["Leaf", "Post-NF-Leaf-Direct.csv"], ["Leaf + EMS", "Post-NF-Leaf-EMS.csv"], ["COVEN (HTTP)", "Post-NF-COVENHTTP-Direct.csv"], ["COVEN (HTTP) + EMS", "Post-NF-COVENHTTP-EMS.csv"], ["COVEN (Socket)", "Post-NF-COVENSocket-Direct.csv"], ["COVEN (Socket) + EMS", "Post-NF-COVENSocket-EMS.csv"]]
for fileResource in processFiles:
	#Opening CSV file
	csvFile =  [line.split(";")[1:] for line in open(fileResource[1], "r").readlines()]
	
	#Preprocessing CSV data
	csvFile[0][0] = float(csvFile[0][0][:-1]) * 1000
	csvFile[1][0] = float(csvFile[1][0][:-1]) * 1000
	csvFile[2] = csvFile[2][:-1]
	for index in range(len(csvFile[2])):
		csvFile[2][index] = float(csvFile[2][index]) * 1000

	#Updating file data
	fileResource.append(csvFile)

makeBar(processFiles)
makeHistogram(createIntervals(processFiles, 10, 450), 450, ['COO','COO + EMS', "Leaf", "Leaf + EMS", "COVEN (HTTP)", "COVEN (HTTP) + EMS", "COVEN (Socket)", "COVEN (Socket) + EMS"])
makeCDF(createCDFIntervals(createIntervals(processFiles, 10, 450), 120), 450, ['COO','COO + EMS', "Leaf", "Leaf + EMS", "COVEN (HTTP)", "COVEN (HTTP) + EMS", "COVEN (Socket)", "COVEN (Socket) + EMS"])