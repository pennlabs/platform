import { useMemo } from "react";
import Select from "react-select";
import { useResourceList } from "@pennlabs/rest-hooks";
import { FieldArray } from "formik";
import { selectStyles } from "../ui";


interface SelectOption {
  id: number;
  name: string;
}

const toSelectOptions = (options) => (
  options.map(obj => ({ value: obj.name, label: obj.name }))
);

export const FormikSelectInput = ({ route, fieldName }) => {
  const { data: rawData } = useResourceList<SelectOption>(route, (id) => `${route}/${id}`);
  const data = rawData || [];

  const options = useMemo(() => {
    return toSelectOptions(data);
  }, [data]);

  return (
    <FieldArray name={fieldName}>
      {({ form, push, remove }) => {
        const values = form.values[fieldName] || [];
        return (
          <Select
            defaultOptions
            isMulti
            styles={selectStyles}
            options={options}
            value={toSelectOptions(values)}
            onChange={(_, { action, option }) => {
              if (action === "select-option") {
                push(data.filter((obj) => obj.name === option.value)[0]);
              } else if (action === "remove-value") {
                remove(values.findIndex((obj) => obj.name === option.value));
              }
            }}
          />
        )

      }}
    </FieldArray>
  );

}
