import { Construct } from "constructs";
import { App, Stack, Workflow } from "cdkactions";
import { DeployJob, DjangoProject } from "@pennlabs/kraken";

export class PlatformStack extends Stack {
  constructor(scope: Construct, name: string) {
    super(scope, name);
    const workflow = new Workflow(this, 'build-and-deploy', {
      name: 'Build and Deploy',
      on: 'push',
    });

    const platformJob = new DjangoProject(workflow, {
      projectName: 'Platform',
      imageName: 'platform',
    });

    new DeployJob(workflow, {}, {
      needs: [platformJob.publishJobId]
    });
  }
}

const app = new App();
new PlatformStack(app, 'platform');
app.synth();
