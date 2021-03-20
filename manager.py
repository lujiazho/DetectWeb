from flask_script import Manager
from flask_migrate import MigrateCommand
from detectweb import create_app

app = create_app()
manager = Manager(app)
# 添加db命令
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
