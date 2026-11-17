from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_docker_manifests_use_the_shared_reverse_proxy_network():
    dockerfile = ROOT / "Dockerfile"
    compose = ROOT / "docker-compose.yml"
    nginx = ROOT / "docker" / "nginx" / "default.conf"

    assert dockerfile.is_file()
    assert compose.is_file()
    assert nginx.is_file()

    compose_text = compose.read_text(encoding="utf-8")
    assert "VIRTUAL_HOST" in compose_text
    assert "VIRTUAL_PORT" in compose_text
    assert "nginx-proxy:" in compose_text
    assert "external: true" in compose_text
    assert "ports:" not in compose_text


def test_static_container_has_a_health_endpoint_and_spa_fallback():
    nginx_text = (ROOT / "docker" / "nginx" / "default.conf").read_text(encoding="utf-8")
    assert "location = /health" in nginx_text
    assert "try_files $uri $uri/ /index.html;" in nginx_text


if __name__ == "__main__":
    test_public_docker_manifests_use_the_shared_reverse_proxy_network()
    test_static_container_has_a_health_endpoint_and_spa_fallback()
    print("Deployment manifest test passed.")
