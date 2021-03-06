#!/bin/sh
#
# TinyCM Plugin - Users and admin Dashboard.
#

if [ "$(GET dashboard)" ]; then
	d="Dashboard"
	header
	html_header
	user_box
	docs=$(find $wiki -type f | wc -l)
	wikisize="$(du -sh $wiki | awk '{print $1}')"
	cachesize="$(du -sh $cache | awk '{print $1}')"
	[ "$HG" != "yes" ] && hg=$(gettext "disabled")
	[ "$HG" = "yes" ] && hg=$(gettext "enabled")
	# Source all plugins.conf to get DASHBOARD_TOOLS and ADMIN_TOOLS
	ADMIN_TOOLS=""
	DASHBOARD_TOOLS=""
	for p in $(ls $plugins)
	do
		[ -f "$plugins/$p/$p.conf" ] && . $plugins/$p/$p.conf
	done
	if check_auth && ! admin_user; then
		ADMIN_TOOLS=""
	fi
	if check_auth; then
		cat << EOT
<div id="tools">
	<a href='$script?log'>Activity log</a>
	<a href='$script?ls'>Pages list</a>
	$DASHBOARD_TOOLS
	$ADMIN_TOOLS
</div>

<h2>$d</h2>

<pre>
Wiki docs        : $docs ($wikisize)
Cache size       : $cachesize
Users account    : $(ls $PEOPLE | wc -l)
Mercurial        : $hg
</pre>
EOT
		
		# Only for admins
		if admin_user; then
			# List all plugins
			cat << EOT
<h3>$(gettext "Plugins:") $(ls $plugins | wc -l)</h3>
<div id="plugins">
<table>
	<thead>
		<td>$(gettext "Name")</td>
		<td>$(gettext "Description")</td>
		<td>$(gettext "Action")</td>
	</thead>
EOT
			for p in $(ls -1 $plugins)
			do
				if [ -f "$plugins/${p}/${p}.conf" ]; then
					. $plugins/${p}/${p}.conf
					cat << EOT
	<tr>
		<td><a href='?$p'>$PLUGIN</a></td>
		<td>$SHORT_DESC</td>
		<td>TODO</td>
	</tr>
EOT
				fi
			done
			echo "</table></div>"
		fi
	else
		gettext "You must be logged in to view the dashboard"
	fi
	html_footer && exit 0
fi
