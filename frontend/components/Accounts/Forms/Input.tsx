import { useField } from "formik";

import { FormInput } from "../ui";

export const FormikInput = function ({ fieldName, ...props }) {
    const [field, meta] = useField(fieldName);

    return (
        <FormInput
            /* eslint-disable */
            {...field}
            {...props}
            /* eslint-enable */
            error={meta.touched && meta.error !== undefined}
        />
    );
};
