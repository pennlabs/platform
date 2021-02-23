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
