import { Construct } from 'constructs';
import { App } from 'cdk8s';
import { CronJob, DjangoApplication, PennLabsChart, ReactApplication } from '@pennlabs/kittyhawk';

const cronTime = require('cron-time-generator');

export class MyChart extends PennLabsChart {
  constructor(scope: Construct) {
    super(scope);

    const domain = "platform.pennlabs.org"
    const devDomain = "platform-dev.pennlabs.org"
    
    const frontendImage = "pennlabs/platform-frontend"
    const backendImage = "pennlabs/platform-backend"
    const devImage = "pennlabs/platform-dev"
    
    const secret = "platform"
    const devSecret = "platform-dev"

    new DjangoApplication(this, 'django', {
      port: 443,
      deployment: {
        image: backendImage,
        secret,
        secretMounts: [
          {
            name: "platform",
            subPath: "SHIBBOLETH_CERT",
            mountPath: "/etc/shibboleth/sp-cert.pem",
          },
          {
            name: "platform",
            subPath: "SHIBBOLETH_KEY",
            mountPath: "/etc/shibboleth/sp-key.pem",
          }
        ]
      },
      domains: [{ 
        host: domain, 
        paths: [
          "/admin",
          "/accounts",
          "/assets",
          "/identity",
          "/s",
          "/options",
          "/openapi",
          "/documentation",
          "/Shibboleth.sso",
          "/healthcheck",
        ],
        isSubdomain: true,
      }],

      ingressProps: {
        annotations: {
          ["ingress.kubernetes.io/protocol"]: "https",
          ["traefik.ingress.kubernetes.io/router.middlewares"]: "default-redirect-http@kubernetescrd"
        },
      },
      djangoSettingsModule: 'Platform.settings.production',
    });

    new ReactApplication(this, 'react', {
      deployment: {
        image: frontendImage,
        replicas: 1,
      },
      domain: {
        host: domain,
        paths: ["/"]
      },
    })

    new DjangoApplication(this, 'dev', {
      port: 8080,
      deployment: {
        image: devImage,
        secret: devSecret,
        env: [{
          name: "DEV_LOGIN",
          value: "true"
        }]
      },
      domains: [{ 
        host: devDomain, 
        paths: ["/"],
        isSubdomain: true,
      }],
      djangoSettingsModule: 'Platform.settings.staging',
    });

    new CronJob(this, 'clear-expired-tokens', {
      schedule: cronTime.everySundayAt(5),
      image: backendImage,
      secret,
      cmd: ["python3", "manage.py", "cleartokens"],
    });
  }
}

const app = new App();
new MyChart(app);
app.synth();
