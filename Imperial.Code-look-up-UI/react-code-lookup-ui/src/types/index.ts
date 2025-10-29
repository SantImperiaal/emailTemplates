export interface LookupFormInputs {
    A2: string;
    B2: string; // Expected format: YYYY-MM-DD
    C2: string; // Expected format: YYYY-MM-DD
    D2: string; // Expected format: YYYY-MM-DD or specific string
    E2: string; // Expected format: YYYY-MM-DD
    F2: string; // Expected format: YYYY-MM-DD
}

export interface LookupResponse {
    eligible: boolean;
    message: string;
    instalmentDate?: string; // Optional, only if eligible
}