let Sentry;

const SENTRY_URL =
    "https://a022d59af8cd4b6e928837a44239d8ac@sentry.pennlabs.org/12";
const dev = process.env.NODE_ENV !== "production";

if (process.browser) {
    // If the code is running in user's browser
    Sentry = require("@sentry/browser");
} else {
    // If code is running on the server
    Sentry = require("@sentry/node");
}

if (!dev) {
    // Sentry.init({ dsn: SENTRY_URL });
}

export function logException(ex: Error, context?: any): void {
    // Sentry.captureException(ex, {
    //     extra: context,
    // });
    // window.console && console.error && console.error(ex); // eslint-disable-line no-console
}

export function logMessage(msg: string): void {
    // Sentry.captureMessage(msg);
}
