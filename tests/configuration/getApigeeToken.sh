#!/bin/bash

# Check for a folder apigee-token-management in $HOME directory
apigee_get_token_dir=$(find $HOME -name 'apigee-token-management')

if [ -z $apigee_get_token_dir ]; then
    # Prompt user to download get_token
    echo "
        It looks like you don't have apigee's get_token utility installed where this script is looking for it.

        If you would like the get_token utility automatically installed to $HOME/apigee-token-management, press [y]. Press any other key to exit. 
        You must have unzip installed on your system (enter command  \"which unzip\" to check).
    "
    read -p "
        Download get_token to $HOME/apigee-token-management? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

    current_directory=$(pwd)

    # Download zip to $HOME/apigee-token-management
    echo "DOWNLOADING ZIP TO $HOME/apigee-token-management"
    cd $HOME
    mkdir apigee-token-management
    cd apigee-token-management
    curl -s -f https://login.apigee.com/resources/scripts/sso-cli/ssocli-bundle.zip -O
    if [ $? -ne 0 ]; then
        echo "an error has occured and the curl has failed."
    fi

    # Unzip download
    echo "UNZIPPING..."
    unzip ssocli-bundle.zip

    # Install get_token
    echo "INSTALLING TO usr/local/bin"
    sudo ./install -b /usr/local/bin

    # Return to previous directory
    cd $current_directory
fi

# export correct login url.
SSO_LOGIN_URL="https://login.apigee.com"
export SSO_LOGIN_URL

# Get new token. Will prompt for username, password and mfa if refresh token is expired.
APIGEE_ACCESS_TOKEN=$(~/apigee-token-management/get_token) 

# Manipulate environment file to include result of executable
sed -i '/^APIGEE_ACCESS_TOKEN/d' ./.env
echo "APIGEE_ACCESS_TOKEN=$APIGEE_ACCESS_TOKEN" >> ./.env

echo "access token refreshed"