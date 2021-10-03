import { App } from "cdkactions";
import { LabsApplicationStack } from "@pennlabs/kraken";

const app = new App();
new LabsApplicationStack(app, {
  djangoProjectName: 'Platform',
  dockerImageBaseName: 'platform',
});

app.synth();
