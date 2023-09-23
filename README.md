# README.md
![Prototype](https://github.com/gadmin7/Transapp/blob/main/Images/isl.gif)

## Table of Contents

- [About](#about)
  - [Directory Structure](#structure)
  - [Dataset](#dataset)
- [Installation](#installation)
  
## About

An attempt to formulate a technological solution to provide Real-time translation to remove:
- **Linguistic barriers:** Add ease of communication by providing various means of language translation such as text, image, or document-enabled input.
- **Sign language barriers:** Using machine learning to translate sign language to text as well as NLP to translate text to sign language.

### Structure
![Project Directory](https://github.com/gadmin7/Transapp/blob/main/Images/proj_directory.png)

The system of TransApp can be broadly divided into three parts:
1. Digital Interface (Web Application)
2. Web Server
3. Backend Modules
   - Rest APIs
   - Sign Language Detection Model
   - English Text to Indian Sign Language Conversion Module
   - Translation Helper Functions ( Language text Input, Image Input, Document Input) 

API has the following routes - (/home, /translate, /pdftranslate, /ocrtranslate, /t2s, /s2t, /video_feed)

## Installation

To get started with this dummy project, follow these steps:

1. Clone the repository from GitHub.
2. Set the Java path in the `eng2isl.py` module: `java_path = r"C:\Program Files\Android\Android Studio\jre\bin"`.
3. Add sign videos for the Text to Sign module to the `txt_sign` folder.
4. Download Stanford Parser 4.2.0 and add its contents to the `txt2_sign` folder.


## Dataset
