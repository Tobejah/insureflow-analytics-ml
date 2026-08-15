'use client';

import { UserMode } from '../../components/user-mode/UserMode';

/**
 * Portfolio-friendly route for the customer-facing insurance recommendation UI.
 * It intentionally reuses UserMode rather than introducing a second dashboard
 * implementation, so the existing agent/API architecture stays unchanged.
 */
export default function DashboardPage() {
  return <UserMode mode='user' />;
}
