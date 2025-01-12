// This file is auto-generated by @hey-api/openapi-ts

import { createClient, createConfig, type Options } from '@hey-api/client-fetch';
import type { GetAlertsGetData, GetAlertsGetError, GetAlertsGetResponse, StartAlertsCheckJobPostError, StartAlertsCheckJobPostResponse, AckAlertAlertIdPatchData, AckAlertAlertIdPatchError, AckAlertAlertIdPatchResponse } from './types.gen';

export const client = createClient(createConfig());

/**
 * Get Alerts
 */
export const getAlertsGet = <ThrowOnError extends boolean = false>(options?: Options<GetAlertsGetData, ThrowOnError>) => {
    return (options?.client ?? client).get<GetAlertsGetResponse, GetAlertsGetError, ThrowOnError>({
        ...options,
        url: '/'
    });
};

/**
 * Start Alerts Check Job
 */
export const startAlertsCheckJobPost = <ThrowOnError extends boolean = false>(options?: Options<unknown, ThrowOnError>) => {
    return (options?.client ?? client).post<StartAlertsCheckJobPostResponse, StartAlertsCheckJobPostError, ThrowOnError>({
        ...options,
        url: '/'
    });
};

/**
 * Ack Alert
 */
export const ackAlertAlertIdPatch = <ThrowOnError extends boolean = false>(options: Options<AckAlertAlertIdPatchData, ThrowOnError>) => {
    return (options?.client ?? client).patch<AckAlertAlertIdPatchResponse, AckAlertAlertIdPatchError, ThrowOnError>({
        ...options,
        url: '/{alert_id}'
    });
};