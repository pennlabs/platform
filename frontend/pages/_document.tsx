import Document, {
    Html,
    Head,
    Main,
    NextScript,
    DocumentContext,
} from "next/document";
import { ServerStyleSheet } from "styled-components";

// extension of next's Document using Styled Components
export default class MyDocument extends Document {
    static async getInitialProps(ctx: DocumentContext) {
        const sheet = new ServerStyleSheet();
        const originalRenderPage = ctx.renderPage;

        try {
            ctx.renderPage = () =>
                originalRenderPage({
                    enhanceApp: (App) => (props) =>
                        /* eslint-disable */
                        sheet.collectStyles(<App {...props} />),
                    /* eslint-enable */
                });

            const initialProps = await Document.getInitialProps(ctx);
            return {
                ...initialProps,
                styles: (
                    <>
                        {initialProps.styles}
                        {sheet.getStyleElement()}
                    </>
                ),
            };
        } finally {
            sheet.seal();
        }
    }

    render() {
        return (
            <Html>
                <Head />
                <body>
                    <Main />
                    <NextScript />
                    <style jsx global>
                        {`
                            #__next {
                                height: 100vh;
                            }
                            html,
                            body {
                                height: 100vh;
                                overflow: hidden;
                            }
                        `}
                    </style>
                </body>
            </Html>
        );
    }
}
