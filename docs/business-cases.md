# Business Case Analyses

## Host Comparison

{{ read_csv("res/hosting-info.csv", keep_default_na=False) }}

## Email Service Providers

Key Takeaways:

- Two options: use a major service provider (Gmail, etc.) or self-host.
- For commercial hosting:
    - There are more security and privacy risks, especially with identifying "this group is taking an action we deem inappropriate".
    - Much easier and simpler to set up and start using.
- For self-hosting:
    - There are fewer risks of identification.
    - The technical architecture and components of getting an email out the door is relatively simple.
    - Many services exist that cover hosting and softare.
    - The hard part is ensuring major email services (Gmail, etc.) don't mark emails from our domain as spam (in inboxes) or simply ban our domain entirely.

Both are vulnerable to the same negative outcome of "we can't contact people". Redundancy within the scope of email providers, and other communication channels, can help reduce risk.

### Commercial Services

- Commercial services (ordered: Gmail, MS, Apple, all others) dominate deliverability.
- Top independent email provider can hope for up to 80% deliverability.
- Getting that "decent" deliverablity means doing everything correctly per these larger firms, because...
- The standards and practices that define deliverablity are controlled by the big players.
- We should assume that new "email security" protocols will come to exist.
- I tend to assume that changes will come specifically if/when other players (e.g. proton) become important market factors or self-hosting email has a boom, etc.
- It is mainly dominace over mailbox hosting (the receiving side) that drives their market dominance. By refusing to receive email from self-hosted mail senders (MX) large firms effectively require us to use their MX in at least a send-via relationship.

The drawback of the big-name email service providers is related to security and privacy. Sending emails through their services risks giving away what we're doing and identifying a large fraction of our customers. Using, e.g., Google for mass mailing means giving Google a list of email addresses. Many of these are Gmail addresses, which are connected to Google accounts, which are connected to real names, addresses, and phone numbers.

There is always a risk of people receiving these emails, since the same is true. But at least with self-hosting an email send-by server, Google would have to do more work to put the pieces together.

### Toward Self-Hosted Email Service

- Email is a point-to-point protocol.
    - Any "distribution network" is expressly defined by specific email senders/receivers.
    - Such networks are not "built in" to the internet.
    - The email headers in the "final" emails we receive are "collected" bounced within email host/vendor networks.
- The history of anti-spam brings us "spam scoring" as a first technology.
    - For self-hosting email receviers/mailboxes this is the first thing we need to get right.
    - As soon as mailserver is up you will start getting spam.
    - Point-to-point emails between two+ self-hosting people/orgs work reliably as soon as we can ignore spam well.
- Delivery to non-self-hosted mail servers is where the "security" comes in. This does not apply to the receiving side, necessarily.
    - "IP reputation" is the next hurdle after the "email security" technologies.
    - The only way to build reputation is to get email successfully delivered by the host/vendor doing the reputation tracking.
    - These vendors dominate their own mail gateways so getting any type of positive reputation score is very hard while getting a bad and rapidly dropping score is quite easy.
- Here are the critical email security concepts to research.
    - [SPF - start here](http://www.open-spf.org/Introduction/). Adding DNS records that declare relationships between domain name and mail servers.
    - [DKIM - harder](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail). Getting your mail server to sign each message originating from your domain.
    - [DMARC - more DNS records](https://en.wikipedia.org/wiki/DMARC). Combines SPF and DKIM.
    - These three are about as good as it gets for self-hosting deliverablity.
    - Next, we send a bunch of email and ask any Gmail (etc.) users we emailed to check their spam folders and press "not spam" on our emails.This helps a great deal but takes a lot of repetition.
    - Unless we have a registered domain name and the ability to create custom DNS records, it's effectively impossible to get secure email setup.
    - Further reading:
        - <https://www.cloudflare.com/learning/email-security/dmarc-dkim-spf/>
        - <https://mxtoolbox.com/dmarc/details/what-is-dmarc>

Self-hosting has security advantages that cannot be had otherwise (mainly you can have personal trust with each person who has root on the mail handling maxhines). This is significant enough that may be worth it to ask the technology team to learn more and get great at self-hosting email. If we think longer term, to the point that many local and regional GS-US and allied groups have built federated infrastructure, then email delivery between these will work just fine. If we start using, e.g., Google for sendmail transport from self-hosted applications, then we can build mail servers to receive GSUS mail next. To start that work we will need a serious discussion of [identiy management](https://en.wikipedia.org/wiki/Identity_and_access_management). Will we support some type of single-signon for GSUS email if/when we start s3lf-hosting it?

#### Potential Pitfalls of Self-Hosting

Once a domain gets flagged as a spammer, it can be very difficult to get it fixed. So while we could do 95% of everything correctly, we could still get the whole domain flagged and then we won't be able to reach anyone.

### Email Send-by Service Tools

- <https://sendportal.io/>
- <https://mautic.org/>
- <https://www.odoo.com/app/email-marketing>
- <https://listmonk.app/>
