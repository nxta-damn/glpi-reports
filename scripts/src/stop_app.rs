use::std::process::{Command, ExitStatus};
use std::env;
use std::fs;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

fn main() -> Result<()> {
    load_env(".env.dev")?;

    docker_compose(&["-f", "deployments/docker-compose.dev.yaml", "down"])?;

    Ok(())
}

fn load_env(env_file: &str) -> Result<()> {
    let contents = fs::read_to_string(env_file)?;
    for line in contents.lines() {
        if line.starts_with('#') || line.trim().is_empty() {
            continue;
        }

        if let Some((key, value)) = line.split_once('=') {
            env::set_var(key.trim(), value.trim());
        }
    }
    Ok(())
}

fn docker_compose(args: &[&str]) -> Result<ExitStatus> {
    Command::new("docker")
        .arg("compose")
        .args(args)
        .envs(env::vars())
        .status()
        .map_err(Into::into)
}
