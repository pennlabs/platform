import { useMemo } from "react";
import Select from "react-select";
import { useResourceList } from "@pennlabs/rest-hooks";
import { useField, FieldArray } from "formik";
import { selectStyles } from "../ui";

interface SelectOption {
    id: number;
    name: string;
}

const toSelectOptions = (options) =>
    options.map((obj) => ({ value: obj.name, label: obj.name }));

export const FormikSelectInput = function ({ route, fieldName }) {
    const { data: rawData } = useResourceList<SelectOption>(
        route,
        (id) => `${route}${id}/`
    );
    const [field, , helper] = useField(fieldName);
    const data = useMemo(() => rawData || [], [rawData]);
    const options = useMemo(() => toSelectOptions(data), [data]);

    return (
        <FieldArray name={fieldName}>
            {({ push, remove }) => {
                const values = field.value || [];
                return (
                    <Select
                        defaultOptions
                        isMulti
                        styles={selectStyles}
                        options={options}
                        value={toSelectOptions(values)}
                        onChange={(_, action) => {
                            if (action.action === "select-option") {
                                push(
                                    data.filter(
                                        (obj) =>
                                            obj.name === action.option.value
                                    )[0]
                                );
                            } else if (action.action === "remove-value") {
                                remove(
                                    values.findIndex(
                                        (obj) =>
                                            obj.name ===
                                            action.removedValue.value
                                    )
                                );
                            } else if (action.action === "clear") {
                                helper.setValue([]);
                            }
                        }}
                    />
                );
            }}
        </FieldArray>
    );
};
