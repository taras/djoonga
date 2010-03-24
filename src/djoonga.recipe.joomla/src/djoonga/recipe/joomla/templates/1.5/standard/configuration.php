<?php
/**
* @version		$Id: configuration.php-dist 11687 2009-03-11 17:49:23Z ian $
* @package		Joomla
* @copyright	Copyright (C) 2005 - 2008 Open Source Matters. All rights reserved.
* @license		GNU/GPL, see LICENSE.php
* Joomla! is free software and parts of it may contain or be derived from the
* GNU General Public License or other free or open source software licenses.
* See COPYRIGHT.php for copyright notices and details.
*
*/
class JConfig {
	/**
	* -------------------------------------------------------------------------
	* Site configuration section
	* -------------------------------------------------------------------------
	*/
	/* Site Settings */
	var $offline = '%(offline)';
	var $offline_message = '%(offline_message)';
	var $sitename = '%(sitename)';			// Name of Joomla site
	var $editor = '%(editor)';
	var $list_limit = '%(list_limit)';
	var $legacy = '%(legacy)';

	/**
	* -------------------------------------------------------------------------
	* Database configuration section
	* -------------------------------------------------------------------------
	*/
	/* Database Settings */
	var $dbtype = '%(dbtype)';					// Normally mysql
	var $host = '%(dbhost)';				// This is normally set to localhost
	var $user = '%(dbuser)';							// MySQL username
	var $password = '%(dbpass)';						// MySQL password
	var $db = '%(dbname)';							// MySQL database name
	var $dbprefix = '%(prefix)';					// Do not change unless you need to!

	/* Server Settings */
	var $secret = '%(secret)'; 		//Change this to something more secure
	var $gzip = '%(gzip)';
	var $error_reporting = '%(error_reporting)';
	var $helpurl = '%(helpurl)';
	var $xmlrpc_server = '%(xmlrpc_server)';
	var $ftp_host = '%(ftp_host)';
	var $ftp_port = '%(ftp_port)';
	var $ftp_user = '%(ftp_user)';
	var $ftp_pass = '%(ftp_pass)';
	var $ftp_root = '%(ftp_root)';
	var $ftp_enable = '%(ftp_enable)';
	var $tmp_path	= '%(tmp_path)';
	var $log_path	= '%(log_path)';
	var $offset = '%(offset)';
	var $live_site = '%(live_site)'; 					// Optional, Full url to Joomla install.
	var $force_ssl = %(force_ssl);		//Force areas of the site to be SSL ONLY.  0 = None, 1 = Administrator, 2 = Both Site and Administrator

	/* Session settings */
	var $lifetime = '%(filetime)';					// Session time
	var $session_handler = '%(session_handler)';

	/* Mail Settings */
	var $mailer = '%(mail)';
	var $mailfrom = '%(mailform)';
	var $fromname = '%(fromname)';
	var $sendmail = '%(sendmail)';
	var $smtpauth = '%(smtpauth)';
	var $smtpuser = '%(smtpuser)';
	var $smtppass = '%(stmppass)';
	var $smtphost = '%(smtphost)';

	/* Cache Settings */
	var $caching = '%(caching)';
	var $cachetime = '%(cachetime)';
	var $cache_handler = '%(cache_handler)';

	/* Debug Settings */
	var $debug      = '%(debug)';
	var $debug_db 	= '%(debug_db)';
	var $debug_lang = '%(debug_lang)';

	/* Meta Settings */
	var $MetaDesc = '%(metadesc)';
	var $MetaKeys = '%(metakeys)';
	var $MetaTitle = '%(metatitle)';
	var $MetaAuthor = '%(metauthor)';

	/* SEO Settings */
	var $sef = '%(sef)';
	var $sef_rewrite = '%(sef_rewrite)';
	var $sef_suffix = '%(sef_suffix)';

	/* Feed Settings */
	var $feed_limit   = %(feed_limit);
	var $feed_email   = '%(feed_email)';
}
?>
