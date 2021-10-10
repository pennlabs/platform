import { useField } from "formik";

import { FormInput } from "../ui";

export const FormikInput = ({ fieldName, ...props }) => {
    const [field, meta] = useField(fieldName);

    // TODO: form validation (year should be constrained to current + 10)
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
