# RNEL Percept Mapping Touch Interface 
[![DOI](https://zenodo.org/badge/260802298.svg)](https://zenodo.org/badge/latestdoi/260802298)

Python and [Kivy](https://kivy.org/#home) based touch interface for reporting location and modality of percepts evoked via spinal cord stimulation in upper or lower limb amputees

<p align="center"><img src="http://g.recordit.co/quCRdtG1qV.gif" width="684" height="486"></p>

## Getting Started

The RNEL-PerceptMapper is a simple multitouch interface that allows researchers to document the location and perceptual quality of sensations evoked via electrical stimulation of the nervous system. This GUI was developed at the University of Pittsburgh's [Rehab Neural Engineering labs](http://www.rnel.pitt.edu) for studies focused on restoring sensation via spinal cord stimulaion in upper and lower limb amputees. 
For each repetition of stimulation, the subject can mark the location of the sensory percept with a free-hand drawing indicating the outline of the evoked percept on an image of the appropriate body segment, i.e., hand, arm, leg, sole etc. The percept quality can be recorded using several commonly used descriptors: touch, pressure, sharp, electrical, tickle, itch, pins and needles, movement, temperature, pain due to stimulation, phantom limb pain and can be modified to add custom descriptors. Each descriptor has an associated scale ranging from 0–10 to record the corresponding perceived intensity. This set of descriptors have been used [previously](https://iopscience.iop.org/article/10.1088/1741-2552/aa966a) to characterize evoked sensory percepts

### Citation
If you use this work in your research, please cite it as follows:

Chandrasekaran, S., Nanivadekar, A., McKernan, G. P., Helm, E. R., Boninger, M. L., Collinger, J. L., Gaunt, R. A., Fisher, L. E. Sensory restoration by epidural stimulation of dorsal spinal cord in upper-limb amputees. [MedRxiv](https://www.medrxiv.org/content/10.1101/19009811v1.abstract)

Copyright (c) 2016 RNEL (University of Pittsburgh)

----------


### Prerequisites
```
python <= 3.5
```
### Installing

-   Clone this repo to your local machine using `https://github.com/pitt-rnel/perceptmapper.git`
 -  Install the packages in requirements.txt 
	- pip : `pip install requirements.txt`
	- conda: `conda install --file requirements.txt`
-  run `python perceptmapping.py`

If setup worked, you should be able to see the GUI shown above. If you experience issues during installation and/or use of RNEL-PerceptMapper, you can post a new issue on the [RNEL PerceptMapper Github issues webpage](https://github.com/pitt-rnel/perceptmapper/issues). We will reply to you as soon as possible.

## Usage

### Layout
The GUI layout is specified in the *perceptmap.kv* file. The PerceptMapper GUI can be divided into 3 parts:

 1. **Receptive field canvas**  
This is where subjects can mark the location of the sensory percept with a free-hand drawing indicating the outline of the evoked percept on an image of the appropriate body segment. By default there are 6 tabs corresponding to the 6 images that can be displayed. 
The perceptmap.ini file contains the default configuration along with the images to be displayed in each tab. To change the images that are displayed on the canvas simply copy over your desired image to the ImageBank folder and edit the *imgfiles* configuration in perceptmap.ini.

 2. **Quality panel**  
 The quality panel is the default panel that is visible on the left hand side of the GUI when launched. It contains a series of radiobuttons and sliders where the subject can describe how natural the sensation felt, whether the stimulaton was painful etc
 
 3. **Modality panel**  
 The modality pane can be accessed by clicking the 'Modality' button at the bottom of the Quality panel. This panel contains a series of commonly used descriptors with associated sliders to describe the percept and report the intensity.

### Configuration
The first time perceptmapper is run, it will generate a perceptmap.ini file that contains the following default configuration:

 - *imgfiles*
	 - default = *['Rpalmar', 'Rdorsum', 'Farms', 'Barms', 'Lpalmar', 'Ldorsum']*
	 - List of filenames for receptive field images to display in the canvas. By default, Perceptmapper will look for pngs in the ImageBank folder .
 - *tablabels* 
	 - default = *['Right\nPalm', 'Right\nDorsum', 'Arms\nFront', 'Arms\nBack', 'Left\nPalm', 'Left\nDorsum']* 
	 - List of strings to be displayed on the tab buttons to toggle between canvas images
 - *savepath* 
	 - default = *../data*
	 - filepath where output files are saved. if the folder does not exist it will be created when the GUI is first launched
 - *trialnumber* 
	 - default = *0*
	 - counter for the number of completed trials. This value is updated every time the GUI is closed and trial numbering will begin from this value the next time PerceptMapper is launched. 
	 - **Be very careful when changing this field manually since you could end up overwriting existing files**
 - *windowborderless* 
	 - default = *False*
	 - When True, this launches the GUI without a menu bar. Useful when running in fullscreen mode.
 - *mmip*
	 - default = *localhost*
	 - If you want to run perceptmapper in *auto* mode the IP address of the module controlling GUI events would be entered here
 - *windowcolor* 
	 - default = *(1, 1, 1, 1)*
	 - Background color for the canva
 - *windowsize*
	 - default = *(1368, 912)*
	 - window size in pixels

### Events
Specific touch events and the corresponding GUI behavior can be customized based on trial design. A few standard GUI events are described here.

 - **Drawing and Erasing**  
Simply touch and drag the tip of the stylus (or finger) anywhere in the receptive field canvas. To erase a drawn line click on the '*Clear current line*' button in the bottom right  

  <p align="center"><img src="http://g.recordit.co/YwLogScov7.gif" width="684" height="486">
</p>
  
 - **Add Sensation**  
On occasion, for a given trial the subject may report 2 distinct sensations. In such instances clicking on the '*Add sensation*' button in the bottom right will save the current canvas along with the quality and modality and reset the GUI to default view so that a second sensation may be entered.  

 <p align="center"><img src="http://g.recordit.co/7Vhif4HxTL.gif" width="684" height="486"></p>    
 
 - **Save data/End trial/Reset GUI**  
At the end of the trial, pressing the '*Save and Reset*' button will save the pixel coordinates of all the lines drawn on the canvas to a *\<trialname>_imPixel.yml* file. All the quality and modality data will be saved to a separate *\<trialname>_RadioCheckSlider.yml* file and a screenshot of every canvas image where a line was drawn, will be saved to a *\<trialname>_\<imgname>.png*  file.  
Further, the GUIs internal counter for trial will be incremented and the GUI will be reset to default view.  

 <p align="center">
  <img src="http://g.recordit.co/dwaDeNopYP.gif" width="684" height="486">
</p>    


 - The PerceptMapper GUI was designed to use [RNEL-Dragonfly](https://github.com/pitt-rnel/rnel_dragonfly) to run in *auto* mode where the GUI state is triggered by a separate module that controls stimulation and trial progress. In this mode, the GUI runs a separate thread to listen to these triggers and update the GUI state. If you would like a demo of this setup or need advice getting a similar setup working, you can post a new issue on the [RNEL PerceptMapper Github issues webpage](https://github.com/pitt-rnel/perceptmapper/issues) or [contact us]().    

 
### Versions
There are 2 versions of the PerceptMapper available [here](https://github.com/pitt-rnel/perceptmapper/tags). 

 - [v1.0](https://github.com/pitt-rnel/perceptmapper/releases/tag/v1.0)  
This version is a specific implementation of the PerceptMapper GUI used in experiments involving spinal cord stimulation for sensory restoration in upper limb amputees and referenced [here](https://www.medrxiv.org/content/10.1101/19009811v1.abstract).  
  <p align="center">
  <img src="http://g.recordit.co/FiMy6DxC1i.gif" width="128" height="243">
  <img src="http://g.recordit.co/CLQDucCbWJ.gif" width="342" height="243">
 </p>    
  
 - [v2.0](https://github.com/pitt-rnel/perceptmapper/releases/tag/v2.0)  
This version includes an update to the modality panel to include more  [descriptors](https://iopscience.iop.org/article/10.1088/1741-2552/aa966a) and gets rid of the *mechanical*, *movement* and *tingle* subdivisions found in the previous version. The list of modalities is currently hard coded but can be made user configurable.  

<p align="center">
  <img src="http://g.recordit.co/vagQgnOZ3t.gif" width="128" height="243">
  <img src="http://g.recordit.co/3BYiWtEmAp.gif" width="342" height="243">
 </p>    

## Built With
* [Kivy](https://kivy.org/#home) - Cross-platform Python Framework for NUI Development

## Author
* **Ameya Nanivadekar** - *Design and deployment* - [acnani](https://github.com/acnani)


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
