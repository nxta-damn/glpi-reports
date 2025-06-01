use::std::process::{Command, ExitStatus};
use std::env;
use std::fs;
use std::thread;
use std::time::Duration;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

fn main() -> Result<()> {
    load_env(".env.test")?;

    docker_compose(&["-f", "deployments/docker-compose.test.yaml", "up", "--build", "-d"])?;

    thread::sleep(Duration::from_secs(5));

    let test_status = run_tests()?;

    docker_compose(&["-f", "deployments/docker-compose.test.yaml", "down"])?;

    if !test_status.success() {
        std::process::exit(1);
    }
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


fn run_tests() -> Result<ExitStatus> {
    Command::new("uv")
        .arg("run")
        .arg("pytest")
        .status()
        .map_err(Into::into)
}
