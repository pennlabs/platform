import { useResourceList } from "@pennlabs/rest-hooks";
import React, { useEffect, useMemo, useState } from "react";
import { Form } from "react-bulma-components";
import { Control, Controller, FieldPath } from "react-hook-form";
import Select from "react-select";

import { User } from "../../../types";

interface DataOption {
    id: number;
    name: string;
}

export interface MultiSelectProps<T> {
    control: Control<T>;
    route: string;
    name: FieldPath<User>;
    disabled?: boolean;
}

const toSelectOptions = (options: DataOption[]) =>
    options.map((obj) => ({ value: obj.id, label: obj.name }));

const MultiSelectInput = (props: MultiSelectProps<User>) => {
    const { control, name, route, disabled } = props;
    const { data: rawData } = useResourceList<DataOption>(
        route,
        (id) => `${route}${id}/`
    );

    const optionsData = useMemo(() => rawData || [], [rawData]);
    const selectOptions = useMemo(
        () => toSelectOptions(optionsData),
        [optionsData]
    );

    const [loading, setLoading] = useState(true);
    useEffect(() => {
        if (rawData) setLoading(false);
    }, [rawData]);

    return (
        <Controller
            name={name}
            control={control}
            render={({ field, fieldState: { error } }) => {
                const fieldValue = (field.value as DataOption[]) || [];
                return (
                    <>
                        <Select
                            instanceId={`select-${name}`}
                            isMulti
                            {...field}
                            value={fieldValue.map(
                                ({ id, name }) =>
                                    selectOptions.find(
                                        ({ value }) => value === id
                                    ) || {
                                        label: name,
                                        value: name,
                                    }
                            )}
                            onChange={(evt) => {
                                if (evt === undefined) return;
                                field.onChange(
                                    evt.map(({ value }) =>
                                        optionsData.find(
                                            ({ id }) => id === value
                                        )
                                    )
                                );
                            }}
                            options={selectOptions}
                            isDisabled={disabled || loading}
                        />
                        <Form.Help color="danger">
                            {error ? error.message : ""}
                        </Form.Help>
                    </>
                );
            }}
        />
    );
};

export default MultiSelectInput;
