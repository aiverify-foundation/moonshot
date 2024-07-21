import logging
import os

import uvicorn
from dotenv import dotenv_values, load_dotenv

from .app import create_app
from .container import Container
from .logging_conf import configure_app_logging, create_uvicorn_log_config
from .services.utils.file_manager import create_temp_dir
from .types.types import UvicornRunArgs


def start_app():
    load_dotenv()
    container: Container = Container()
    # use our own config.yml
    config_file = dotenv_values().get("MS_WEB_API_CONFIG")
    if config_file is None:
        container.config.from_default()
    else:
        container.config.from_yaml(f"{config_file}", required=True)

    create_temp_dir(container.config.temp_folder())
    configure_app_logging(container.config)
    logging.info(f"Environment: {container.config.app_environment()}")
    ENABLE_SSL = container.config.ssl.enabled()
    SSL_CERT_PATH = container.config.ssl.file_path()
    app = create_app(container.config)

    run_kwargs: UvicornRunArgs = {}
    port = dotenv_values().get("HOST_PORT", 5000)
    if port is not None:
        port = int(port)
    run_kwargs["port"] = port
    run_kwargs["host"] = dotenv_values().get("HOST_ADDRESS", "127.0.0.1")
    run_kwargs["log_config"] = create_uvicorn_log_config(container.config)
    if ENABLE_SSL:
        if not SSL_CERT_PATH:
            logging.debug("SSL_CERT_PATH not set, not enabling SSL")
        elif os.path.exists(os.path.join(SSL_CERT_PATH, "key.pem")) and os.path.exists(
            os.path.join(SSL_CERT_PATH, "cert.pem")
        ):
            run_kwargs["ssl_keyfile"] = str(
                os.path.join(SSL_CERT_PATH, str(container.config.ssl.key_filename()))
            )
            run_kwargs["ssl_certfile"] = str(
                os.path.join(SSL_CERT_PATH, str(container.config.ssl.cert_filename()))
            )
        else:
            logging.debug(
                "SSL_CERT_PATH does not contain necessary files, not enabling SSL"
            )
    uvicorn.run(app, **run_kwargs)  # type: ignore


if __name__ == "__main__":
    start_app()
