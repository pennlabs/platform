import { useMemo } from "react";
import Select from "react-select";
import { useResourceList } from "@pennlabs/rest-hooks";
import { useField, FieldArray } from "formik";
import { selectStyles } from "../ui";


interface SelectOption {
  id: number;
  name: string;
}

const toSelectOptions = (options) => (
  options.map(obj => ({ value: obj.name, label: obj.name }))
);

export const FormikSelectInput = ({ route, fieldName }) => {
  const { data: rawData } = useResourceList<SelectOption>(route, (id) => `${route}${id}/`);
  const [field, meta, helper] = useField(fieldName);
  const data = rawData || [];

  const options = useMemo(() => {
    return toSelectOptions(data);
  }, [data]);

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
            onChange={(_, { action, option, removedValue }) => {
              if (action === "select-option") {
                push(data.filter((obj) => obj.name === option.value)[0]);
              } else if (action === "remove-value") {
                remove(values.findIndex((obj) => obj.name === removedValue.value));
              } else if (action === "clear") {
                helper.setValue([]);
              }
            }}
          />
        )

      }}
    </FieldArray>
  );

}
