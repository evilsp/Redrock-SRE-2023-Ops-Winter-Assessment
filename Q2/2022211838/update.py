import pkg_resources
import subprocess
import time
def update_image(image_name):
    current_image_version = subprocess.check_output(["docker", "inspect", image_name, "--format", "{{.Config.Labels.version}}"]).strip()
    latest_image_version = subprocess.check_output(["curl", "-s", "https://registry.hub.docker.com/v2/repositories/{}/tags/".format(image_name), "-H", "Accept: application/vnd.docker.distribution.manifest.v2+json"]).strip()
    if pkg_resources.parse_version(current_image_version) < pkg_resources.parse_version(latest_image_version):
        subprocess.call(["docker", "pull", image_name])
        print("已更新")
    else:
        print("镜像已是最新版本")
while True:
    update_image('project/myproject')
    time.sleep(604800)