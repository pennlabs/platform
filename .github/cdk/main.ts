import { App, Stack, Workflow } from "cdkactions";
import { DeployJob, DjangoProject, DockerPublishJob, ReactProject } from "@pennlabs/kraken";
import { Construct } from "constructs";

const app = new App();
class PlatformStack extends Stack {
  public constructor(scope: Construct, name: string) {
    super(scope, name);

    const workflow = new Workflow(this, "build-and-deploy", {
      name: "Build and Deploy",
      on: "push",
    });

    const backend = new DjangoProject(workflow, {
      projectName: "Platform",
      path: "backend",
      imageName: "platform-backend",
    });

    const publishPlatformDev = new DockerPublishJob(workflow, 'platform-dev', {
      imageName: "platform-dev",
      path: "backend",
      dockerfile: "Dockerfile.dev"
    },
      {
        needs: "django-check"
      });

    const frontend = new ReactProject(workflow, {
      path: "frontend",
      imageName: "platform-frontend",
    });

    new DeployJob(
      workflow,
      {},
      {
        needs: [
          backend.publishJobId,
          frontend.publishJobId,
          publishPlatformDev.id,
        ],
      }
    );

  }
}

new PlatformStack(app, 'platform')
app.synth();
