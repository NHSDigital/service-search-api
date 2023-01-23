const env_regex = /^([a-zA-Z]+)(?=(\.api\.service\.nhs\.uk))/gm
var hostname_env = str.replace(env_regex, request.headers.host)
context.setVariable("request_hostname_env", hostname_env);
