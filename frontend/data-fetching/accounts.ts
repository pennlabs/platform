import { ContactType } from "../types";
import { doApiRequest } from "../utils/fetch";

export const verifyContact = async (
    type: ContactType,
    id: number,
    code: string
) => {
    const payload = { verification_code: code };
    const res = await doApiRequest(`/accounts/me/${type}/${id}/`, {
        method: "PATCH",
        body: payload,
    });

    if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail);
    }
};

export const createContact = async (type: ContactType, value: string) => {
    const res = await doApiRequest(`/accounts/me/${type}/`, {
        method: "POST",
        body: { value },
    });

    if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail);
    }

    return res.json();
};

export const deleteContact = async (type: ContactType, id: number) => {
    const res = await doApiRequest(`/accounts/me/${type}/${id}/`, {
        method: "DELETE",
    });

    if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail);
    }
};

export const reverifyContact = async (type: ContactType, id: number) => {
    const res = await doApiRequest(
        `/accounts/me/${type}/${id}/resend_verification/`,
        { method: "POST" }
    );

    if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail);
    }
};
