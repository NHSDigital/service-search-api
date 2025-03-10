#!/bin/bash

# Check for a folder apigee-token-management in $HOME directory
APIGEE_GET_TOKEN_DIR=$(find $HOME -name 'apigee-token-management')

# Check for the get_token tool within this folder
APIGEE_GET_TOKEN_PATH=""
if [ ! -z $APIGEE_GET_TOKEN_DIR ]; then
    APIGEE_GET_TOKEN_PATH=$(find "$HOME/apigee-token-management" -name 'get_token')
fi

# Download necessary tools
if [ -z $APIGEE_GET_TOKEN_DIR ] || [ -z $APIGEE_GET_TOKEN_PATH ]; then
    # Prompt user to download get_token
    echo "
        It looks like you don't have apigee's get_token utility installed where this script is looking for it.

        If you would like the get_token utility automatically installed to $HOME/apigee-token-management, press [y]. Press any other key to exit. 
        
        YOU MUST HAVE UNZIP INSTALLED ON YOUR SYSTEM BEFORE PROCEEDING. Use 'sudo apt install unzip' to install this utility."
    read -p "
        Download get_token to $HOME/apigee-token-management? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

    current_directory=$(pwd)

    # Download zip to $HOME/apigee-token-management
    echo "DOWNLOADING ZIP TO $HOME/apigee-token-management"
    cd $HOME
    if [ -z $APIGEE_GET_TOKEN_DIR ]; then
        mkdir apigee-token-management
    fi
    cd apigee-token-management
    curl -s -f https://login.apigee.com/resources/scripts/sso-cli/ssocli-bundle.zip -O
    if [ $? -ne 0 ]; then
        echo "an error has occured and the curl has failed."
    fi

    # Unzip
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

# Check for .env file.
ENV_FILE_PATH=$(find . -name '.env')
if [ -z $ENV_FILE_PATH ]; then
    touch '.env'
fi

# Delete current APIGEE_ACCESS_TOKEN
sed -i '/^APIGEE_ACCESS_TOKEN/d' ./.env

# Check if .env file ends with newline and add new APIGEE_ACCESS_TOKEN appropriately
if [ -z "$(tail -c 1 < "./.env")" ]; then
    echo "APIGEE_ACCESS_TOKEN=$APIGEE_ACCESS_TOKEN" >> ./.env
else
    echo -e "\nAPIGEE_ACCESS_TOKEN=$APIGEE_ACCESS_TOKEN" >> ./.env
fi

echo "access token refreshed"
