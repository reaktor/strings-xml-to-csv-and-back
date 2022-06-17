# strings.xml to csv

Scripts for creating csv files from Android strings.xml files. Just that, with plain Python 3, no external dependencies.

## Why?

Because [copy pasting from Android Studio Translations editor is no longer supported](https://issuetracker.google.com/issues/37062314), [StackOverflow ](https://stackoverflow.com/questions/30684496/how-to-import-export-android-string-resource-to-excel-for-localization)
does not help, the existing tools found online were abandoned, or too complicated to run, or did too many things, or imposed
structure that did not suit our project. The translation editors would work, but adopting them is not easy. 

## Usage

```
usage: strings_to_csv.py [-h] out_file res_path

Convert strings.xml -files to csv

positional arguments:
  out_file    output file
  res_path    path to res directory, for example "~/AndroidStudioProjects/MyApp/app/src/main/res"

optional arguments:
  -h, --help  show this help message and exit
```
