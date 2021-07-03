using System;
using System.Collections;
using System.ComponentModel;
using System.IO;
using System.Management.Automation; // PowerShellStandard
using System.Security.AccessControl;
using System.Security.Principal;

namespace ClientInstaller
{
    [RunInstaller(true)]
    public partial class Installer1 : System.Configuration.Install.Installer
    {
        public Installer1()
        {
            InitializeComponent();
        }

        [System.Security.Permissions.SecurityPermission(System.Security.Permissions.SecurityAction.Demand)]
        public override void Install(IDictionary stateSaver)
        {
            base.Install(stateSaver);
            SetDirectorySecurity();
            SetHostFile();
            SetDefenderException("install");
        }

        public override void Uninstall(IDictionary savedState)
        {
            base.Uninstall(savedState);
            SetDefenderException("uninstall");
        }

        private void SetDirectorySecurity()
        {
            string targetdir = Path.GetDirectoryName(Context.Parameters["targetdir"]);
            Log("Adding modify rights for " + targetdir);
            // The following code was copied (and modified) from "Jaso" (http://www.aspnet-answers.com/microsoft/NET-Security/30001760/how-to-change-group-permissions-on-existing-folder.aspx).
            // Retrieve the Directory Security descriptor for the directory
            var dSecurity = Directory.GetAccessControl(targetdir, AccessControlSections.Access);
            // Build a temp domainSID using the Null SID passed in as a SDDL string.
            // The constructor will accept the traditional notation or the SDDL notation interchangeably.
            var domainSid = new SecurityIdentifier("S-1-0-0");
            // Create a security Identifier for the BuiltinUsers Group to be passed to the new accessrule
            var ident = new SecurityIdentifier(WellKnownSidType.BuiltinUsersSid, domainSid);
            // Create a new Access Rule.
            // ContainerInherit AND ObjectInherit covers both target folder, child folder and child object.
            // However, when using both (combined with AND), the permissions aren't applied.
            // So use two rules.
            // Propagate.none means child and grandchild objects inherit.
            var accessRule1 = new FileSystemAccessRule(ident, FileSystemRights.Modify, InheritanceFlags.ObjectInherit, PropagationFlags.None, AccessControlType.Allow);
            var accessRule2 = new FileSystemAccessRule(ident, FileSystemRights.Modify, InheritanceFlags.ContainerInherit, PropagationFlags.None, AccessControlType.Allow);
            // Add the access rules to the Directory Security Descriptor
            dSecurity.AddAccessRule(accessRule1);
            dSecurity.AddAccessRule(accessRule2);
            // Persist the Directory Security Descriptor to the directory
            Directory.SetAccessControl(targetdir, dSecurity);
            Log("Rights added.");
            //throw new NotImplementedException();
        }

        private void SetHostFile()
        {
            string hostFile = "c:\\windows\\system32\\drivers\\etc\\hosts";

            // Host file entries
            string localRedirects = "127.0.0.1\tshipment-support-amazon.com covidsupportgermany.de coronahilfengermany.de mpseinternational.com mail.domain.com #MPSE";
            Log("Changing content of hosts file");
            string[] linesHostFile = File.ReadAllLines(hostFile);

            // check if local redirects are present
            Boolean bSettingsSet = false;
            foreach (string line in linesHostFile)
            {
                // replace existing localhost redirects
                if (line.Contains("#MPSE") && (line != localRedirects))
                {
                    Log("Updating 127.0.0.1 entry");
                    Console.WriteLine("updateing");
                    line.Replace(line, localRedirects);
                    bSettingsSet = true;
                }
            }

            File.WriteAllLines(hostFile, linesHostFile);

            // if settings not found append to end
            if (!bSettingsSet)
            {
                Log("Write redirects to end of hosts-file");
                Console.WriteLine("asd");
                StreamWriter sw = File.AppendText(hostFile);
                sw.WriteLine(localRedirects);
                sw.Close();
            }            
        }

        private void SetDefenderException(string sMode)
        {
            using (var ps = PowerShell.Create())
            {
                string cmd = " -ExclusionPath 'C:\\Program Files (x86)\\hda'";
                if (sMode == "install")
                {
                    cmd = "Add-MpPreference" + cmd;
                } else
                {
                    cmd = "Remove-MpPreference" + cmd;
                }
                ps.AddScript(cmd);
                var res = ps.Invoke();

                Log(res.ToString());
            }
        }

        private void Log(string message)
        {
            Context.LogMessage(message);
            System.Diagnostics.Trace.WriteLine(message, "1177 client installer");
        }
    }
}
