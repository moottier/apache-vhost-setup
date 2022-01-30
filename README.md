
# SYNOPSIS

./make_apache_conf **TEMPLATE_PATH** **YML_PATH** **SITE**  

# DESCRIPTION

make_apache_conf loads the template file at **TEMPLATE_PATH** and the YAML file at **YML_PATH**. Values in the template file are substituted with values in the YAML file for the given **SITE** to give a substituted file. The substituted file is written to a path specified in the YAML file.  

## YML Setup  
A top-level **GLOBAL** key is required for execution, although it may be empty. holds parsing settings used for all sites. Site-level settings are defined in any other top-level key. Any **SITE** passed in a call to make_apache_conf must be a top-level 
key in the YAML file.

The **GLOBAL** key is required to have both an **RE_PATTERN** and **FOUT_KEY** as children. 

**RE_PATTERN** key holds a regex used to locate values in the template file to be substituted. The regex must have a single capturing group which corresponds to the value to be substituted. 

**FOUT_KEY** maps to a **SITE** key whose value defines the file path where that site's config will be written. Change this value if you want to store output paths in another key

<INS>Example:</INS>  
The following will use regex pattern `({\s*.*?\s*})` to find matches in **TEMPLATE_PATH**. If the script is called with **SITE** `www.andremottier.com`, then output is written to `/etc/apache2/sites-available/www.andremottier.com.conf`.  

```yml
GLOBAL:
    RE_PATTERN: ({\s*.*?\s*})
    FOUT_KEY: SitesAvailableFilePath
www.andremottier.com:
    SitesAvailableFilePath: /etc/apache2/sites-available/www.andremottier.com.conf
    RedirectPermanent: https://www.andremottier.com
    ServerName: dev.andremottier.com
dev.andremottier.com:
    SitesAvailableFilePath: /etc/apache2/sites-available/dev.andremottier.com.conf
    RedirectPermanent: https://www.andremottier.com
    ServerName: dev.andremottier.com    
```

## Pattern Matching  
The mattern matched for substitution can be set by changing the GLOBAL.RE_PATTERN value in the YAML file.

The RE_PATTERN value must be valid regex.

# TESTS  
Run python -m unittest test.py
