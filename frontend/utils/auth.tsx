import {
    GetServerSidePropsContext,
    GetServerSidePropsResult,
    Redirect,
} from "next";
import { doApiRequest } from "./fetch";
import { User } from "../types";

export interface AuthProps {
    user: User;
}

type GetServerSidePropsResultDiscUnion<T> =
    | { tag: "props"; props: T }
    | { tag: "redirect"; redirect: Redirect }
    | { tag: "notFound"; notFound: true };

function convertGetServerSidePropsResult<T>(
    r: GetServerSidePropsResult<T>
): GetServerSidePropsResultDiscUnion<T> {
    if (Object.prototype.hasOwnProperty.call(r, "props")) {
        const casted = r as { props: T };
        return { tag: "props", props: casted.props };
    } else if (Object.prototype.hasOwnProperty.call(r, "redirect")) {
        const casted = r as { redirect: Redirect };
        return { tag: "redirect", redirect: casted.redirect };
    } else if (Object.prototype.hasOwnProperty.call(r, "notFound")) {
        return { tag: "notFound", notFound: true };
    }

    throw new Error("NextJS typing information incorrect");
}

type GetServerSidePropsFunc<T> = (
    ctx: GetServerSidePropsContext
) => Promise<GetServerSidePropsResult<T>>;

export function withAuth<T>(getServerSidePropsFunc: GetServerSidePropsFunc<T>) {
    return async (
        ctx: GetServerSidePropsContext
    ): Promise<GetServerSidePropsResult<T & AuthProps>> => {
        if (ctx.resolvedUrl === "/health") {
            const wrapped = await getServerSidePropsFunc(ctx);
            const casted = convertGetServerSidePropsResult(wrapped);

            if (casted.tag === "props") {
                return {
                    props: { ...casted.props },
                };
            } else if (casted.tag === "notFound") {
                return { notFound: casted.notFound };
            } else {
                return { redirect: casted.redirect };
            }
        }

        const headers = {
            credentials: "include",
            headers: { cookie: ctx.req.headers.cookie },
        };

        const res = await doApiRequest("/accounts/me/", headers);
        if (res.ok) {
            const user = await res.json();
            const wrapped = await getServerSidePropsFunc(ctx);
            const casted = convertGetServerSidePropsResult(wrapped);

            if (casted.tag === "props") {
                return {
                    props: { ...casted.props, user },
                };
            } else if (casted.tag === "notFound") {
                return { notFound: casted.notFound };
            } else {
                return { redirect: casted.redirect };
            }
        } else {
            return {
                redirect: {
                    destination: `/accounts/login/?next=${ctx.resolvedUrl}`,
                    permanent: false,
                },
            };
        }
    };
}
