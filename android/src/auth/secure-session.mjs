import {Capacitor,registerPlugin} from '@capacitor/core';
import {createSecureVault} from './vault-queue.mjs';
const SecureSession=registerPlugin('SecureSession');
// Browser previews hold tokens in memory only. Android never uses browser storage.
export const secureSessionVault=Capacitor.isNativePlatform()?createSecureVault(SecureSession):null;
