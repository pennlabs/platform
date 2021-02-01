import { Option } from "../types";
import { doApiRequest } from "../utils/fetch";

interface NamedObject {
    name: string;
}

const generateLoadOption = (route: string) => {
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
            value: obj.name,
        }));
    };
    return loadOptionFunc;
};

export default generateLoadOption;
