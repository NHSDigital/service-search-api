const env_regex = /^([a-zA-Z]+)(?=(\.api\.service\.nhs\.uk))/gm;
var hostname_env = request.headers.host;
hostname_env.replace(env_regex, request.headers.host);
context.setVariable("request_hostname_env", hostname_env);
