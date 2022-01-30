
# SYNOPSIS

./make_apache_conf <INS>TEMPLATE_PATH</INS> <INS>YML_PATH</INS> <INS>SITE</INS>  

# DESCRIPTION

make_apache_conf loads the template file at <INS>TEMPLATE_PATH</INS> and the YAML file at <INS>YML_PATH</INS>. Values in the template file are substituted with values in the YAML file for the given <INS>SITE</INS> to give a substituted file. The substituted file is written to a path specified in the YAML file.  

**YML Setup**  
A top-level GLOBAL key holds parsing settings used for all sites. Site-level settings are defined in any other top-level key. Any <INS>SITE</INS> passed in a call to make_apache_conf must be a top-level 
key in the YAML file.

The RE_PATTERN key holds the regex value used to find values to be substituted.  

The FOUT_KEY maps to a <INS>SITE</INS> key whose value defines the file path where that site's config will be written. Change this value if you want to store output paths in another key

The following will use regex pattern `({\s*.*?\s*})` to find matches in <INS>TEMPLATE_PATH</INS>. If the script is called with <INS>SITE</INS> `www.andremottier.com`, then output is written to `/etc/apache2/sites-available/www.andremottier.com.conf`.  

Example:

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

**Pattern Matching**  
The mattern matched for substitution can be set by changing the GLOBAL.RE_PATTERN value in the YAML file.

The RE_PATTERN value must be valid regex.

# TESTS  
Run python -m unittest test.py
