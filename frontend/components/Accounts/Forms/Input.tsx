import { useField } from "formik";
import React from "react";

import { FormInput } from "../ui";

export const FormikInput = ({
    fieldName,
    ...props
}: { fieldName: string } & React.ComponentPropsWithoutRef<"input">) => {
    const [field, meta] = useField(fieldName);

    return (
        // TODO: make this neater
        // @ts-ignore
        <FormInput
            /* eslint-disable */
            {...field}
            {...props}
            /* eslint-enable */
            error={meta.touched && meta.error !== undefined}
        />
    );
};
