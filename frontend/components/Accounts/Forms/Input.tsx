import { useField } from "formik";

import { FormInput } from "../ui";

export const FormikInput = ({ fieldName, ...props }: { fieldName: string }) => {
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
