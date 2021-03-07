import { ContactType, NamedObject, Option } from "../types";
import { doApiRequest } from "../utils/fetch";

export const generateLoadOption = (route: string) => {
    const loadOptionFunc = async (inputValue: string): Promise<Option[]> => {
        if (inputValue.length === 0) {
            return [];
        }
        const objects: NamedObject[] = await doApiRequest(
            `/accounts/${route}/?search=${inputValue}`
        )
            .then((res) => res.json())
            .catch((_) => []);

        return objects.map((obj) => ({
            label: obj.name,
            value: obj.id,
        }));
    };
    return loadOptionFunc;
};

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
    // TODO: use `value` field on both models?
    const key = type === ContactType.Email ? "email" : "phone_number";
    const payload = { [key]: value };
    const res = await doApiRequest(`/accounts/me/${type}/`, {
        method: "POST",
        body: payload,
    });

    if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail);
    }
};

export const makePrimaryContact = async (type: ContactType, id: number) => {
    const payload = { primary: true };
    const res = await doApiRequest(`/accounts/me/${type}/${id}/`, {
        method: "PATCH",
        body: payload,
    });

    if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail);
    }
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
