import { useField } from "formik";

import { FormInput } from "../ui";

export const FormikInput = ({ fieldName, ...props }) => {
    const [field, meta] = useField(fieldName);

    return (
        <FormInput
            {...field}
            {...props}
            error={meta.touched && meta.error !== undefined}
        />
    );
};
