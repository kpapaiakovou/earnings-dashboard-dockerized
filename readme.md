################################################################################
# installation
################################################################################

see the _installation directory for installation instructions

################################################################################
# overview
################################################################################

The app keeps track of earnings, royalties, billing, and reports & statements for users

Users have balance accounts, which can be of either a Royalties Payable or Accounts Receivable type.
Depending on the type the data for that balance account will show up on the royalties or billing page

There are three types of data entries that can be made to a balance account which use different models
that have a one-to-one relationship with the base entry, 1) Earnings, 2) Payments, 3) Adjustments.
Earnings entries will always show up on the earnings page regardless of the balance account type which
provides a consistent earnings view experience across different types of customer relationships. Then
depending on the balance account type, the summarized balance and list of all entries to it are shown
on either the royalties page or billing page. Entries should never be made directly to the core balance
entry model, instead all entries should be made as one of the three types which django-admin provides
an inline form to achieve which automatically creates both the specific entry type and core entry record.

There is also reports page which allows listing any type of file download to make available to the user
which generally would be PDF reports, invoices and statements, and detailed CSV files.

When entries are entered, they can be specified as whether to be visible or not to the user yet
and can also be specified as to whether they have been reviewed reconciled or not by an accountant.
Any visible entries are assumed to have been reconciled. Other than making entries visible or not,
whether a non-visible entry has been reconciled or not currently has no effect other than an admin
being able to see the value of this property.

The import-export library has been installed but has not been implemented in order to allow bulk
uploading lists of entries via a CSV template. This would save the accounting team a lot of time.
The idea of how this would work on conjunction with the reconciliation status is that good practice
would be for any bulk added entries to be initially set to unreconciled, then an accountant would
review and verify them as reconciled (but still not yet visible), and then finally there would be
a command that can be run via the push of a button to automatically update all reconciled entries
to visible.

################################################################################
# user accounts for testing
################################################################################

django-admin (url: /admin)
u: admin
p: admin

test users for main site
u: EXTREME_MUSIC
p: earningstest
note: has a royalties balance

u: SONY_ATV_PUBLISHING
p: earningstest
note: has a billing balance