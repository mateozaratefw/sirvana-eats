import datetime


def parse_expires(expires_str):
    """
    Convert the 'Expires' column (e.g. 2025-08-28T22:59:56.694Z) to an int UNIX timestamp.
    If 'Expires' is 'Session', return None (session cookie with no explicit expiry).
    """
    expires_str = expires_str.strip()
    if expires_str.lower() == "session" or not expires_str:
        return None
    # Remove trailing 'Z' and parse
    # e.g. "2025-08-28T22:59:56.694Z" -> "2025-08-28T22:59:56.694+00:00"
    iso_str = expires_str.replace("Z", "+00:00")
    dt = datetime.datetime.fromisoformat(iso_str)
    return int(dt.timestamp())


def parse_samesite(samesite_str):
    """
    Playwright accepts 'Lax', 'Strict', or 'None' for sameSite.
    Return None if it's blank or invalid.
    """
    val = samesite_str.strip().capitalize()  # e.g. 'lax' -> 'Lax'
    if val in ["Lax", "Strict", "None"]:
        return val
    return None


def parse_checkmark(value_str):
    """Return True if the cell has a '✓', else False."""
    return "✓" in value_str


COOKIE_TABLE = """AF_SYNC	1741365704323	.rappi.com.ar	/	2025-03-14T16:41:44.000Z	20						Medium	
AMP_101be7b7fd	JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI3Mjg1MzE2ZC1iZWQwLTQyYjctYTY0My01NTJjNTBlZmQ5MDAlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJBUl80OTg3NDYyMTQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQxNDc4ODM1OTgwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc0MTQ3ODk0ODc4MiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTYwJTJDJTIycGFnZUNvdW50ZXIlMjIlM0EwJTdE	.rappi.com.ar	/	2026-03-09T00:09:08.000Z	342			Lax			Medium	
AMP_8f241b95e3	JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyM2EyYjkwYi1lN2NmLTRmNjktODAwOS1iN2E1ODM4MjMyY2UlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM5MTE4NDI2MzkxJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczOTExODQyNjQ3NyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMiUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMSU3RA==	.amplitude.com	/	2026-02-09T16:27:06.000Z	294			Lax			Medium	
AMP_MKTG_101be7b7fd	JTdCJTdE	.rappi.com.ar	/	2026-03-07T16:41:43.000Z	27			Lax			Medium	
AMP_MKTG_8f241b95e3	JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE	.amplitude.com	/	2026-02-09T16:27:06.000Z	163			Lax			Medium	
AMP_MKTG_c64663a7bf	JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE	.amplitude.com	/	2026-02-09T16:27:06.000Z	163			Lax			Medium	
AMP_MKTG_e3e918f274	JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE	.amplitude.com	/	2026-02-09T16:27:06.000Z	163			Lax			Medium	
AMP_c64663a7bf	JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJmYWY2ZGE2ZS05MTY2LTRhMjItYmVkNC02ZTE2ZTJkMDExNTAlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM5MTE4NDI2NDc3JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczOTExODQyNjU0MiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMiUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMSU3RA==	.amplitude.com	/	2026-02-09T16:27:06.000Z	294			Lax			Medium	
AMP_e3e918f274	JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJmYWY2ZGE2ZS05MTY2LTRhMjItYmVkNC02ZTE2ZTJkMDExNTAlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM5MTE4NDI2NDc2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczOTExODQzNjg5MiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzIlMkMlMjJwYWdlQ291bnRlciUyMiUzQTElN0Q=	.amplitude.com	/	2026-02-09T16:27:16.000Z	294			Lax			Medium	
CookieControl	{"necessaryCookies":["_utmzz","utmzzses","corp_utm","membership_token*","sj_csrftoken","amp_ps","g_csrf_token","access_token_local"],"optionalCookies":{"performance":"accepted","functional":"accepted","advertising":"accepted"},"ccpa":{"shown":true,"updated":"25/04/2018"},"statement":{"shown":true,"updated":"25/04/2018"},"consentDate":1739118436873,"consentExpiry":90,"interactedWith":true,"user":"21C0FC41-6A34-4ADA-86F9-8F5D4B742533"}	.amplitude.com	/	2025-05-10T16:27:16.000Z	454			Lax			Medium	
MR	0	.bat.bing.com	/	2025-03-13T16:14:42.380Z	3		✓	None			Medium	
MSPTC	HX5dK4ISd64mQUq-OpRU5EZq6DJjWQdaM4PqrmgbJsA	.bing.com	/	2026-02-21T22:18:38.549Z	48		✓	None	https://rappi.com.ar	✓	Medium	
MUID	223316D1C25B69E92E3C03A1C3FE681B	.bing.com	/	2026-03-31T16:14:42.380Z	36		✓	None			High	
Path	/	www.rappi.com.ar	/	Session	5		✓				Medium	
__utmzz	utmcsr=google|utmcmd=organic|utmccn=(not set)|utmctr=(not provided)	.amplitude.com	/	2025-08-08T16:27:09.000Z	74						Medium	
__utmzzses	1	.amplitude.com	/	Session	11						Medium	
_ga	GA1.3.1168790922.1741365704	.rappi.com.ar	/	2026-04-13T00:09:08.765Z	30						Medium	
_ga	GA1.2.1686453322.1739118429	.amplitude.com	/	2026-03-16T16:27:10.770Z	30						Medium	
_ga_2FY44PPV92	GS1.1.1739118429.1.1.1739118440.49.0.0	.amplitude.com	/	2026-03-16T16:27:20.361Z	52						Medium	
_ga_EH4F8E7F7Z	GS1.1.1741478835.8.1.1741478948.32.0.0	.rappi.com.ar	/	2026-04-13T00:09:08.232Z	52						Medium	
_ga_FGJHX7E4KW	GS1.1.1741478835.8.1.1741478948.23.0.0	.rappi.com.ar	/	2026-04-13T00:09:08.773Z	52						Medium	
_ga_KLC0Z8KSQ7	GS1.1.1741478835.8.1.1741478948.0.0.0	.rappi.com.ar	/	2026-04-13T00:09:08.219Z	51						Medium	
_ga_Y9SY6M64LX	GS1.1.1741478835.8.1.1741478948.0.0.0	.rappi.com.ar	/	2026-04-13T00:09:08.770Z	51						Medium	
_gat_UA-64467188-13	1	.rappi.com.ar	/	2025-03-09T00:09:40.000Z	20						Medium	
_gat_UA-64467188-7	1	.rappi.com.ar	/	2025-03-09T00:09:38.000Z	19						Medium	
_gcl_au	1.1.355559676.1741365704	.rappi.com.ar	/	2025-06-05T16:41:43.000Z	31						Medium	
_gid	GA1.3.604305659.1741365704	.rappi.com.ar	/	2025-03-10T00:09:08.000Z	30						Medium	
lr_hb-ttasrx%2Frappi-webv	{%22heartbeat%22:1741478948024}	www.rappi.com.ar	/	2025-03-10T00:09:08.000Z	58			Lax			Medium	
lr_tabs-ttasrx%2Frappi-webv	{%22recordingID%22:%226-0195783a-3291-73ae-afd4-8caf0460b93a%22%2C%22sessionID%22:0%2C%22lastActivity%22:1741478965075%2C%22hasActivity%22:true}	www.rappi.com.ar	/	2025-03-10T00:09:25.000Z	173			Lax			Medium	
lr_uf-ttasrx	d20b059c-89c8-4e9f-a820-56026bdf300d	www.rappi.com.ar	/	Session	50			Lax			Medium	
_mkto_trk	id:138-CDN-550&token:_mch-amplitude.com-a4dca4f53c91fa6cfb780e1783edc418	.amplitude.com	/	2026-03-16T16:27:09.288Z	81						Medium	
_tt_enable_cookie	1	.rappi.com.ar	/	2026-04-03T00:09:08.000Z	18						Medium	
_ttp	2rXlFbI4hwex6v1Pdkb9Mlm7oGb	.tiktok.com	/	2026-04-03T00:09:08.398Z	31		✓	None			Medium	
ttp	01JNRQQXAHV07HE297HZ6V9SGP.tt.2	.rappi.com.ar	/	2026-04-03T00:09:08.000Z	36						Medium	
_uetsid	0db5e3e0fb7311ef8d53b9efa0b38dd4	.rappi.com.ar	/	2025-03-10T00:09:08.000Z	39						Medium	
_uetvid	b6482940e70211efa93177df5513c0ae	.amplitude.com	/	2026-03-06T16:27:10.000Z	39						Medium	
_uetvid	a8381540dcfc11efab8b3974c0098d8f	.rappi.com.ar	/	2026-04-03T00:09:08.000Z	39						Medium	
ab.storage.deviceId.f6a1117f-52de-444c-9fbd-49d465e7f80e	%7B%22g%22%3A%2292b3a65c-b1e5-556f-f030-69a637043eed%22%2C%22c%22%3A1741478958589%2C%22l%22%3A1741478958589%7D	.rappi.com.ar	/	2026-03-09T05:58:18.000Z	166						Medium	
ab.storage.sessionId.f6a1117f-52de-444c-9fbd-49d465e7f80e	g%3A485ef378-d198-633e-84d8-d83a8916c3b8%7Ce%3A1741480749097%7Cc%3A1741478948183%7Cl%3A1741478949097	.rappi.com.ar	/	2026-04-13T00:09:09.000Z	157						Medium	
afUserId	412d820c-b94d-4b8d-aac1-2bf3f6a32476-p	.rappi.com.ar	/	2026-04-13T00:09:08.510Z	46						Medium	
af_id	412d820c-b94d-4b8d-aac1-2bf3f6a32476-p	.appsflyer.com	/	2026-04-08T00:09:08.465Z	43		✓	None			Medium	
amplitude_id_101be7b7fdda892d329579012e8dd69arappi.com.ar	eyJkZXZpY2VJZCI6ImJkNGE3NjljLWY1YjctNDRkMS04ZTJiLWJhN2Q4NzU0NTYwZlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0MTQ3ODgzNDk1NiwibGFzdEV2ZW50VGltZSI6MTc0MTQ3ODk0ODE4MCwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9	.rappi.com.ar	/	2026-04-13T00:09:08.180Z	301						Medium	
ar_debug	1	.www.google-analytics.com	/	2025-06-07T00:08:40.545Z	9	✓	✓	None			Medium	
cmpl_token	AgQQAPMdF-RO0tOW7G2OONk5_eidbWOU_4qWYNpY4Q	.tiktok.com	/	2025-03-17T13:09:17.418Z	52	✓	✓				Medium	
currentLocation	JTdCJTIyaWQlMjIlM0E0MzUxNDU1NzElMkMlMjJhZGRyZXNzJTIyJTNBJTIyQ29uY2VwY2klQzMlQjNuJTIwQXJlbmFsJTIwMjk4OSUyQyUyMEMxNDI2JTIwQ2l1ZGFkJTIwZGUlMjBCdWVub3MlMjBBaXJlcyUyQyUyMCUyMEFyZ2VudGluYSUyMiUyQyUyMmFjdGl2ZSUyMiUzQXRydWUlMkMlMjJsYXQlMjIlM0EtMzQuNTc4OTclMkMlMjJsbmclMjIlM0EtNTguNDQyNSUyQyUyMmNvdW50cnklMjIlM0ElMjJBUiUyMiUyQyUyMmRlc2NyaXB0aW9uJTIyJTNBJTIyYWxlcGglMjIlMkMlMjJ0YWclMjIlM0FudWxsJTJDJTIyY2l0eSUyMiUzQSUyMkJ1ZW5vcyUyMEFpcmVzJTIyJTJDJTIyaXNJbml0aWFsTG9jYXRpb24lMjIlM0F0cnVlJTdE	.www.rappi.com.ar	/	2026-03-09T00:09:42.618Z	495			Lax			Medium	
d_ticket	09849c199d37fd8e47bd2557a7b3a60f26705	.tiktok.com	/	2026-01-16T13:09:17.417Z	45	✓					Medium	
deviceid	201c21d5-3d5f-4f4e-9b91-f29ba92876ee	.www.rappi.com.ar	/	2026-03-07T16:41:00.000Z	44		✓	Lax			Medium	
g_state	{"i_l":0}	www.rappi.com.ar	/	2025-09-05T00:07:30.000Z	16						Medium	
guestAuthVersion	2	www.rappi.com.ar	/	2025-03-09T01:09:25.392Z	17						Medium	
msToken	yB6G2kcBYgm4IVKWswBFqjF_5xMWRa8o4KV9olpl6S3vl_LcUTdg_BMB-6z4qIztGWJfKaRWNJaYJOXjFYD1zVqI6AEtQ_8VUsFRMqexDu8hqnoW6_mXM5SbF6Stqlw5pSmzzw29_Xur6RHQ4DXCjqJr	.tiktok.com	/	2025-03-12T03:27:09.282Z	159		✓	None			Medium	
multi_sids	263463644909142016%3A12f9e0f31a826485863a732fc769ec4f	.tiktok.com	/	2025-03-17T13:09:17.418Z	63	✓	✓				Medium	
odin_tt	46be2eff19db5df3315dfdd8af60d253ad4b45265ce63060c1dd0fdab3559174255bf99077aa4c0d3bccc5ae518661f7	.tiktok.com	/	2026-01-18T15:57:35.977Z	103	✓					Medium	
passport_csrf_token	c95291b94341212cdb558d1d339b9937	.tiktok.com	/	2025-03-17T13:06:52.370Z	51		✓	None			Medium	
passport_csrf_token_default	c95291b94341212cdb558d1d339b9937	.tiktok.com	/	2025-03-17T13:06:52.370Z	59		✓				Medium	
rappi.acceptedCookies	1	.www.rappi.com.ar	/	2026-03-07T16:51:25.249Z	22			Lax			Medium	
rappi.data	eyJpZCI6NDk4NzQ2MjE0LCJmaXJzdE5hbWUiOiJNYXRlbyIsImxhc3ROYW1lIjoiWmFyYXRlIiwiZ2VuZGVyIjoiIiwiaWRlbnRpZmljYXRpb25UeXBlIjowLCJpZGVudGlmaWNhdGlvbiI6IiIsImVtYWlsIjoibWF0ZW96YXJhdGVmd0BnbWFpbC5jb20iLCJkZWZhdWx0Q2MiOm51bGwsImxhc3RQdXNoQ3VzdG9tIjpudWxsLCJiaXJ0aGRheSI6bnVsbCwicmVwbGFjZW1lbnRDcml0ZXJpYUlkIjpudWxsLCJyZWZlcmVkQ29kZSI6bnVsbCwicGhvbmUiOiIzNDM1MTM1MTY5IiwicmVtZW1iZXJUb2tlbiI6bnVsbCwiaXNQaG9uZUNvbmZpcm1lZCI6dHJ1ZSwiY2NCbG9ja2VkIjpmYWxzZSwiZGV2aWNlSWQiOiIyMDFjMjFkNS0zZDVmLTRmNGUtOWI5MS1mMjliYTkyODc2ZWUiLCJibG9ja2VkIjpmYWxzZSwiZXhpdG9JZCI6bnVsbCwiZXhpdG9Mb3lhbHR5VHlwZSI6bnVsbCwiYXBwbGljYXRpb24iOiJyYXBwaSIsInZpcCI6ZmFsc2UsInBheXBhbEJsb2NrZWQiOmZhbHNlLCJzdGF0dXNGcmF1ZCI6Im5vdF92ZXJpZmllZCIsImluc3RhbGxtZW50cyI6MSwiY291bnRyeUNvZGUiOiIrNTQiLCJzb2NpYWxQcm92aWRlciI6Imdvb2dsZSIsIm5hbWUiOiJNYXRlbyBaYXJhdGUiLCJwaWMiOiIiLCJyYXBwaUNyZWRpdHMiOiIwIiwicmFwcGlDcmVkaXRBY3RpdmUiOmZhbHNlLCJnbXYiOjAsImNyZWF0ZWRBdCI6IjIwMjQtMDItMTEgMTI6NDc6MDgiLCJhY3RpdmVBZGRyZXNzIjpudWxsLCJsb3lhbHR5Ijp7ImlkIjotMSwibmFtZSI…	.rappi.com.ar	/	2026-03-09T00:07:40.000Z	1626			Lax			Medium	
rappi.id	eyJhY2Nlc3NfdG9rZW4iOiJmdC5nQUFBQUFCbnpOdkQ5NmR4U0pwekc1ckpvN1I1S0YwSlZuTUZrT2hTVkRXUVY0OE5sNVNHSHhjNFI5VWdTU2hhYW1qNUg0dWxrblBfWVVwbGpBTXFZdzBCbjc2OU02VGdkT3FvRDlNdWlFWG1lbUtlXzB0cml2anlYT0xzQS1Ham8xZFBubWZrWDc3RTR6el9HYlBsNnRLaGFpLVBSY1MzZmI4LVk0eXFXclA0bld1eWRobDQ2ZEFNenpROWkyRkFnWDc4YU9yWVNwSmpNbnV3bUEtWnRMSWZmVDFuM3RqU3hpU1lHZEtvVVJPbl9LeTRkaXV2ODVmSTZXR3RMeEd3eW5ETHE4T1IwM2tDQ0VkekNRQXhlMW5vd003MTU3blROdnVhSkVjdW5uTGZPSS1HZENLVzNFWkdfYWQ3clVEdnI4TzVxekFlYkVMTEdYYXROVHljUFg1ZWRBRmdZd3BlQ2FzTnBOZk1tSUIwRG9KVEdkV3dtU1MwYzJlbTN6NDdvRXpwWmI1U3RmN3I2X0htSHB4LUFzbjJZd0ViZW1NQ2tBPT0iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiZXhwaXJlc19pbiI6NjA0ODAwLCJyZWZyZXNoX3Rva2VuIjoiZnQuZ0FBQUFBQm56TnZEQWM3WS1oZG5nYWZCOGpIQUEzb1d0VHNzQzhNWDJOanV3SWttTlNId2xrZ2M0ZGlNVlZ2Q0NyTTVsR2l4eXlOd2hBaHJnaWZwQVE1aTBRWWlwOFQ1aXJWc1pCcFFqSUY1NWhfZ2lReXhiUWNUODktTnFxT1FLQ2pndUxlU2l4eEUyUkE4OFZqSkFiTFBmNC1XWFFnaHZueUZqVDktLXpEdjRrcktkRnNITHdNbkxkWUk3MFBCNVJBZlFMZXg2QjgtRXpPWXg5eGFhXzNsRGNPb3hObzZKSm1ZOE9ZTlJ6UXZ3QXRSZFRqZFU…	.rappi.com.ar	/	2025-06-08T06:07:47.730Z	1272			Lax			Medium	
rappi.type	1	.rappi.com.ar	/	2025-06-08T06:07:47.730Z	11			Lax			Medium	
rappi_refresh_token	ZnQuZ0FBQUFBQm56TnZEQWM3WS1oZG5nYWZCOGpIQUEzb1d0VHNzQzhNWDJOanV3SWttTlNId2xrZ2M0ZGlNVlZ2Q0NyTTVsR2l4eXlOd2hBaHJnaWZwQVE1aTBRWWlwOFQ1aXJWc1pCcFFqSUY1NWhfZ2lReXhiUWNUODktTnFxT1FLQ2pndUxlU2l4eEUyUkE4OFZqSkFiTFBmNC1XWFFnaHZueUZqVDktLXpEdjRrcktkRnNITHdNbkxkWUk3MFBCNVJBZlFMZXg2QjgtRXpPWXg5eGFhXzNsRGNPb3hObzZKSm1ZOE9ZTlJ6UXZ3QXRSZFRqZFUxcldsV0RYQXZ6RElvc3M0RlpVU3l1M1VtTTNHRGFydFFvX1U0bDU0NVRyeUFQN18wQjRHX0xQNERMbWRoVjdGdjhNQkFzS2U4aWdtb2hHaWpKR1hEdmdOV1U3OVJ1Y2NNckJsb0Ric3l5cUM1UWRwc0V0TkxzaXp6dTE5Z2hqRXpGejUwb1U0VUxHTDBFbS0wSlprUUNnR1FtV3FoTkg1QjJ4Vzd3Ym85WjF4QT09	.rappi.com.ar	/	2025-06-08T06:07:47.730Z	583			Lax			Medium	
s_v_web_id	verify_m5zchvu9_zxWA8Fnd_Kutw_42eB_AowA_Wcjc44oRzOWV	.tiktok.com	/	Session	62		✓	None			Medium	
sessionid	12f9e0f31a826485863a732fc769ec4f	.tiktok.com	/	2025-07-15T13:09:17.106Z	41	✓	✓				Medium	
sessionid_ss	12f9e0f31a826485863a732fc769ec4f	.tiktok.com	/	2025-07-15T13:09:17.106Z	44	✓	✓	None			Medium	
sid_guard	12f9e0f31a826485863a732fc769ec4f%7C1737032962%7C15551995%7CTue%2C+15-Jul-2025+13%3A09%3A17+GMT	.tiktok.com	/	2026-01-11T13:09:22.106Z	103	✓	✓				Medium	
sid_tt	12f9e0f31a826485863a732fc769ec4f	.tiktok.com	/	2025-07-15T13:09:17.106Z	38	✓	✓				Medium	
sid_ucp_v1	1.0.0-KDNjODIxOGFiYzc5YmIxMGNhYmVlNTA1YjJhYzA2MTE2MDM1NzQ3YmIKGgiAgKiwoNmA1AMQgoqkvAYYsws4AUDqB0gEEAMaAm15IiAxMmY5ZTBmMzFhODI2NDg1ODYzYTczMmZjNzY5ZWM0Zg	.tiktok.com	/	2025-07-15T13:09:17.106Z	162	✓	✓				Medium	
ssid_ucp_v1	1.0.0-KDNjODIxOGFiYzc5YmIxMGNhYmVlNTA1YjJhYzA2MTE2MDM1NzQ3YmIKGgiAgKiwoNmA1AMQgoqkvAYYsws4AUDqB0gEEAMaAm15IiAxMmY5ZTBmMzFhODI2NDg1ODYzYTczMmZjNzY5ZWM0Zg	.tiktok.com	/	2025-07-15T13:09:17.106Z	163	✓	✓	None			Medium	
store-country-code	ar	.tiktok.com	/	2025-07-15T13:09:17.809Z	20	✓					Medium	
store-country-code-src	uid	.tiktok.com	/	2025-07-15T13:09:17.809Z	25	✓					Medium	
store-idc	maliva	.tiktok.com	/	2025-07-15T13:09:17.808Z	15	✓					Medium	
tt-target-idc	useast1a	.tiktok.com	/	2025-07-15T13:09:17.809Z	21	✓					Medium	
tt-target-idc-sign	eFXjNZyxKRnIHimMwvvzxshH2g243UncGJWhyAurx9uyMLzpJ1IE49E7GeytB-JI-9dV0EogD3DHalWPTSm6IkAAFtglFIQWtuDr28LThdMyzqvnIS0BC0ph15soOl0D-Mgig6KFm_62tABfAmmJzrEOnwiSRM28K4RI5buj1mXi_0wRDXw2YOuocq2A7guu-ZyjIEcVaEKTCzInHDV3M2fFgT-jb9jvR1VvANc6BG4CkJ_lxBpbAZCBVYVZrLdZbifIm20Dgk11LjuM10n_klXUxkABa-59qhqxp6FpSXcpL6QdHZD4tfBmsAOCHKI87sl2WeMfVjPp0fpvwmgzG6cwfoNi0gXE05hhczzwWcmCEp0gWi6sIFIeKVyhbEXzUvY5bPBdUS9D3jxEJ9lkOGYBFDc1zEZ4EShlchQ5T-NRlL5sStFklnOyNs7Pt_sQ7rQGgHrEf8kcBqROKIx-XuWDiPagQRJZ4yqjqt_UTmMLxgIxDOIZs3vd4cGuBqXO	.tiktok.com	/	2026-01-16T13:09:18.318Z	530	✓					Medium	
tt_chain_token	VOGD6G6ZjpKSEbwh/VjojA==	.tiktok.com	/	2025-08-29T03:27:02.965Z	38	✓	✓				Medium	
tt_csrf_token	BmzNo1Vn-LRW2Y0f4aBgch1JjywW9wATXPf0	.tiktok.com	/	Session	49	✓	✓	Lax			Medium	
ttwid	1%7Corht3igrysj9SwFiqLNY1sbh3LUdRn1ulLgfRtreo4Y%7C1740886024%7Ccc9504470d884645348a771d4185d5a055fe9903058ed03bf3a4f8d9a1c3559d	.tiktok.com	/	2026-03-02T03:27:04.774Z	132	✓	✓	None			Medium	
uid_tt	f28aa41f431c45a5bd9d6acd64d421c9e39ea45498aa12150c7bb3ba3e651038	.tiktok.com	/	2025-07-15T13:09:17.106Z	70	✓	✓				Medium	
uid_tt_ss	f28aa41f431c45a5bd9d6acd64d421c9e39ea45498aa12150c7bb3ba3e651038	.tiktok.com	/	2025-07-15T13:09:17.106Z	73	✓	✓	None			Medium"""


def parse_cookie_line(line):
    """
    Given a single line of the cookie table, split the columns and return a dict suitable for Playwright's add_cookies().
    Columns we expect (tab-separated):
      0: name
      1: value
      2: domain
      3: path
      4: expires
      5: size
      6: httpOnly (✓ or blank)
      7: secure   (✓ or blank)
      8: sameSite (Lax / Strict / None / blank)
      (the rest we ignore)
    """
    parts = line.split("\t")
    # Ensure we have at least 9 columns
    if len(parts) < 9:
        return None

    name = parts[0].strip()
    value = parts[1].strip()
    domain = parts[2].strip()
    path = parts[3].strip()
    expires_raw = parts[4].strip()
    # parts[5] is size (we don't need it for set_cookie)
    httpOnly_raw = parts[6]
    secure_raw = parts[7]
    sameSite_raw = parts[8]

    # Build the cookie dict
    cookie = {
        "name": name,
        "value": value,
        "domain": domain,
        "path": path,
    }

    # Expires -> convert if not 'Session'
    expires_ts = parse_expires(expires_raw)
    if expires_ts is not None:
        cookie["expires"] = expires_ts

    # httpOnly / secure / sameSite
    cookie["httpOnly"] = parse_checkmark(httpOnly_raw)
    cookie["secure"] = parse_checkmark(secure_raw)
    samesite_val = parse_samesite(sameSite_raw)
    if samesite_val:
        cookie["sameSite"] = samesite_val

    return cookie


def create_cookies():
    lines = COOKIE_TABLE.strip().splitlines()
    cookies = []

    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        parsed = parse_cookie_line(ln)
        if parsed:
            cookies.append(parsed)

    return cookies


def create_storage():
    """
    Returns a dictionary containing the storage state with predefined values.
    This includes various browser storage items like local storage and session storage entries.
    """
    return {
        "B002E": "AAxORKuG-oJEc7HQVcdiS-vyyKRfXW8bQ9hrJffUUNLw_kbhRov79anobMjSYdD-IdTT8SNpbdRxwMKuYUYjf-AnFE6M2g",
        "AF_SESSION": "1741478948225",
        "AMP_unsent_101be7b7fd": "[]",
        "_gcl_ls": '{"schema":"gcl","version":1,"gcl_ctr":{"value":{"value":4,"creationTimeMs":1741478923562},"expires":1749254923562}}',
        "lr_id": '{"userID":"26833c96-28c7-470a-ad6f-1ae29c6f94d7"}',
        "_uetsid": "0db5e3e0fb7311ef8d53b9efa0b38dd4",
        "_uetsid_exp": "Mon, 10 Mar 2025 00:09:08 GMT",
        "_uetvid": "a8381540dcfc11efab8b3974c0098d8f",
        "_uetvid_exp": "Fri, 03 Apr 2026 00:09:08 GMT",
        "ab.storage.device.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":{"browser":"Chrome","browser_version":"134.0.0.0","os_version":"Mac","resolution":"1512x982","locale":"es","time_zone":"America/Buenos_Aires","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}}',
        "ab.storage.deviceId.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":{"g":"92b3a65c-b1e5-556f-f030-69a637043eed","c":1741478958589,"l":1741478958589}}',
        "ab.storage.globalRateLimitCurrentTokenCount.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":20}',
        "ab.storage.lastReqToEndpoint.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":{"data":1741478949098}}',
        "ab.storage.lastSdkReq.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":1741478949098}',
        "ab.storage.messagingSessionStart.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":1741472067621}',
        "ab.storage.requestAttempts.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":{"data":1}}',
        "ab.storage.sdk_metadata.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":["npm"]}',
        "ab.storage.sessionId.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":"g:485ef378-d198-633e-84d8-d83a8916c3b8|e:1741480749097|c:1741478948183|l:1741478949097"}',
        "ab.storage.session_id_for_cached_metadata.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":"485ef378-d198-633e-84d8-d83a8916c3b8"}',
        "ab.storage.userId.f6a1117f-52de-444c-9fbd-49d465e7f80e": '{"v":"g:AR_498746214|e:undefined|c:1741478865968|l:1741478865969"}',
        "amplitude_unsent_101be7b7fdda892d329579012e8dd69a": "[]",
        "amplitude_unsent_identify_101be7b7fdda892d329579012e8dd69a": "[]",
        "chakra-ui-color-mode": "light",
        "ed73f20edbf2b73": "a1c139f9a3654b7a8652157a2be3464e_1896998885640",
        "ed73f20edbf2b74": "0:1:1741478884547:1741478884547:78310542cbd5c5a9757c995cc38af792",
        "firebase:host:rappi-eta-ar.firebaseio.com": '"s-usc1b-nss-2122.firebaseio.com"',
        "hasEnabledNotifications": "false",
        "i18nextLng": "es",
        "lastExternalReferrer": "other",
        "lastExternalReferrerTime": "1738016326287",
        "mmActionField": '{"coupon":""}',
        "mmCDLoyalty": "undefined",
        "mmCDPrime": "undefined",
        "mmValue": "45523",
        "source": "PROMOTION_BANNER",
    }
